$(document).ready(function () {
    $("#datatable").DataTable(),
        $("#datatable-buttons")
            .DataTable({ lengthChange: !1, buttons: ["copy", "excel", "pdf", "colvis"] })
            .buttons()
            .container()
            .appendTo("#datatable-buttons_wrapper .col-md-6:eq(0)"),
        $(".dataTables_length select").addClass("form-select form-select-sm");
});
$(document).ready(function () {
    $("#datatable1").DataTable(),
        $("#datatable1-buttons")
            .DataTable({ lengthChange: !1, buttons: ["copy", "excel", "pdf", "colvis"] })
            .buttons()
            .container()
            .appendTo("#datatable1-buttons_wrapper .col-md-6:eq(0)"),
        $(".dataTables1_length select").addClass("form-select form-select-sm");
});
$(document).ready(function () {
    $("#datatable2").DataTable(),
        $("#datatable2-buttons")
            .DataTable({ lengthChange: !1, buttons: ["copy", "excel", "pdf", "colvis"] })
            .buttons()
            .container()
            .appendTo("#datatable2-buttons_wrapper .col-md-6:eq(0)"),
        $(".dataTables2_length select").addClass("form-select form-select-sm");
});
$(document).ready(function () {
    $("#datatable3").DataTable(),
        $("#datatable3-buttons")
            .DataTable({ lengthChange: !1, buttons: ["copy", "excel", "pdf", "colvis"] })
            .buttons()
            .container()
            .appendTo("#datatable3-buttons_wrapper .col-md-6:eq(0)"),
        $(".dataTables3_length select").addClass("form-select form-select-sm");
});


