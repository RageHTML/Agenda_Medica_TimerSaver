document.addEventListener("DOMContentLoaded", function () {
    var dados = window.AGENDAMENTOS_DATA || [];

    function normalizar(texto) {
        return (texto || "")
            .toString()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase();
    }

    function formatarStatus(cell) {
        var valor = cell.getValue() || "";
        var classe = "status-badge status-" + normalizar(valor).replace(/\s+/g, "-");
        return '<span class="' + classe + '">' + valor + "</span>";
    }

    var PLACEHOLDER_PADRAO = "Nenhum agendamento encontrado.";
    var PLACEHOLDER_SEM_RESULTADO = "Nenhum registro encontrado para essa busca.";
    var PLACEHOLDER_ERRO_BUSCA = "Não foi possível buscar agora. Tente novamente.";

    var table = new Tabulator("#tabela-agendamentos", {
        data: dados,
        layout: "fitColumns",
        responsiveLayout: "collapse",
        placeholder: PLACEHOLDER_PADRAO,
        columns: [
            { title: "Data", field: "data", width: 110, sorter: "date", sorterParams: { format: "dd/MM/yyyy" } },
            { title: "Horário", field: "horario", width: 90 },
            { title: "Paciente", field: "paciente", minWidth: 160, responsive: 0 },
            { title: "CPF", field: "cpf", width: 130 },
            { title: "Médico", field: "medico", minWidth: 160 },
            { title: "Especialidade", field: "especialidade", minWidth: 140 },
            { title: "Convênio", field: "convenio", width: 120 },
            {
                title: "Status",
                field: "status",
                width: 130,
                hozAlign: "center",
                formatter: formatarStatus,
            },
        ],
    });

    var campoBusca = document.getElementById("busca-agendamentos");
    var debounceTimer = null;

    function buscarAgendamentos(termoOriginal) {
        var termo = (termoOriginal || "").trim();

        if (!termo) {
            table.setData(dados);
            table.setPlaceholder(PLACEHOLDER_PADRAO);
            return;
        }

        var url = "/api/agendamentos?q=" + encodeURIComponent(termo);

        fetch(url)
            .then(function (resposta) {
                if (!resposta.ok) {
                    throw new Error("Resposta inválida do servidor: " + resposta.status);
                }
                return resposta.json();
            })
            .then(function (resultado) {
                table.setPlaceholder(PLACEHOLDER_SEM_RESULTADO);
                table.setData(Array.isArray(resultado) ? resultado : []);
            })
            .catch(function () {
                table.setPlaceholder(PLACEHOLDER_ERRO_BUSCA);
                table.setData([]);
            });
    }

    if (campoBusca) {
        campoBusca.addEventListener("input", function () {
            var valor = campoBusca.value;

            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(function () {
                buscarAgendamentos(valor);
            }, 300);
        });
    }
});