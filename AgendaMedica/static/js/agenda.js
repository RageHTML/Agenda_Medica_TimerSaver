document.addEventListener("DOMContentLoaded", function () {
    function normalizar(texto) {
        return (texto || "")
            .toString()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase();
    }

    function formatarStatus(cell) {
        var valor = cell.getValue();
        if (!valor || valor.trim() === "") {
            valor = "Agendada";
        }
        
        var classe = "status-badge status-" + normalizar(valor).trim().replace(/\s+/g, "-");
        return '<span class="' + classe + '">' + valor + "</span>";
    }

    var table = new Tabulator("#tabela-agendamentos", {
        data: window.AGENDAMENTOS_DATA || [],
        layout: "fitColumns",
        responsiveLayout: "collapse",
        placeholder: "Nenhum registro encontrado.",
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

    function executarBuscaAPI(termo) {
        var url = "/api/agendamentos?q=" + encodeURIComponent(termo);

        fetch(url)
            .then(function (resposta) {
                return resposta.json();
            })
            .then(function (dados) {
                if (Array.isArray(dados) && dados.length > 0) {
                    table.setData(dados);
                } else {
                    table.clearData();
                }
            })
            .catch(function () {
                table.clearData();
            });
    }

    if (campoBusca) {
        campoBusca.addEventListener("input", function () {
            var valor = campoBusca.value.trim();

            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(function () {
                executarBuscaAPI(valor);
            }, 300);
        });

        campoBusca.addEventListener("keydown", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                clearTimeout(debounceTimer);
                executarBuscaAPI(campoBusca.value.trim());
            }
        });
    }
});