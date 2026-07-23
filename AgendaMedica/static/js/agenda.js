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

    // Função auxiliar robusta para converter string de data em carimbo numérico (Timestamp)
    function parseDataParaOrdem(valorStr) {
        if (!valorStr) return 0;
        var s = valorStr.toString().trim();
        
        // Se estiver no formato brasileiro DD/MM/YYYY ou DD/MM/YYYY HH:mm
        if (/^\d{2}\/\d{2}\/\d{4}/.test(s)) {
            var partes = s.split(" ")[0].split("/");
            var hora = s.split(" ")[1] || "00:00:00";
            return new Date(partes[2] + "-" + partes[1] + "-" + partes[0] + "T" + hora).getTime();
        }
        
        // Se estiver no formato padrão ISO YYYY-MM-DD
        return new Date(s).getTime() || 0;
    }

    var table = new Tabulator("#tabela-agendamentos", {
        data: window.AGENDAMENTOS_DATA || [],
        layout: "fitColumns",
        responsiveLayout: "collapse",
        placeholder: "Nenhum registro encontrado.",
        columns: [
            { 
                title: "Data", 
                field: "data", 
                width: 110, 
                // Sorter customizado para garantir que ordene perfeitamente independente do formato da API
                sorter: function(a, b, aRow, bRow, column, dir, sorterParams) {
                    var t1 = parseDataParaOrdem(a);
                    var t2 = parseDataParaOrdem(b);
                    return t1 - t2;
                }
            },
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