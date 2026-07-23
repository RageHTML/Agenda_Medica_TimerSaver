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

    var table = new Tabulator("#tabela-agendamentos", {
        data: dados,
        layout: "fitColumns",
        responsiveLayout: "collapse",
        placeholder: "Nenhum agendamento encontrado.",
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

    // Busca única que filtra por paciente, CPF ou médico simultaneamente
    var campoBusca = document.getElementById("busca-agendamentos");
    if (campoBusca) {
        campoBusca.addEventListener("input", function () {
            var termo = normalizar(campoBusca.value);

            if (!termo) {
                table.clearFilter();
                return;
            }

            table.setFilter(function (linha) {
                return (
                    normalizar(linha.paciente).indexOf(termo) !== -1 ||
                    normalizar(linha.cpf).indexOf(termo) !== -1 ||
                    normalizar(linha.medico).indexOf(termo) !== -1
                );
            });
        });
    }
});