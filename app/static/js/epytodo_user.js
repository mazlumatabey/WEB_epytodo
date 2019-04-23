function modify(id_modify) {
    $.getJSON("/user/task/" + id_modify,
    function(json) {
        document.getElementById("text_central").textContent="Modify this task";
        document.getElementById("title").value=json["result"]["title"];
        document.getElementById("status").value=json["result"]["status"];
        document.getElementById("begin").value=json["result"]["begin"];
        document.getElementById("end").value=json["result"]["end"];
        document.getElementById("button_submit").textContent="Modify";
        document.getElementById("isUpdate").value = id_modify;
    });
}
$(document).ready(function() {
    $('form').on('submit', function(event) {
        var isUpdate = document.getElementById("isUpdate").value;
        if (isUpdate === '0') {
        $.ajax({
                data: {
                    title: $('#title').val(),
                    begin: $('#begin').val(),
                    end: $('#end').val(),
                    status: $('#status').val()
                },
                type: 'POST',
                url: '/user/task/add'
            })
            .done(function(data, text_status, xhr) {
                if (xhr.status == 200)
                    document.location.reload(true)
            });
        event.preventDefault();
    } else {
        $.ajax({
                data: {
                    title: $('#title').val(),
                    begin: $('#begin').val(),
                    end: $('#end').val(),
                    status: $('#status').val()
                },
                type: 'POST',
                url: '/user/task/' + $('#isUpdate').val()
            })
            .done(function(data, text_status, xhr) {
                if (xhr.status == 200)
                    document.location.reload(true)
            });
        event.preventDefault();
    }});
});
$(document).ready(function() {
    $.getJSON("/my_user/my_get_tasks",
        function(json) {
            var tr = [];
            var status;
            var begin;
            var end;
            for (var i = 0; i < json.length; i++) {
                if (json[i]["begin"])
                    begin = json[i]["begin"];
                else
                    begin = "Not defined";
                if (json[i]["end"])
                    end = json[i]["end"];
                else
                    end = "Not defined";
                switch (json[i]["status"]) {
                    case 0:
                        status = "Not started";
                        break;
                    case 1:
                        status = "In progress";
                        break;
                    case 2:
                        status = "Done";
                        break;
                }
                switch (json[i]["status"]) {
                    case 0:
                        tr.push('<tr class="bg-info">');
                        break;
                    case 1:
                        tr.push('<tr class="bg-warning">');
                        break;
                    case 2:
                        tr.push('<tr class="bg-success">');
                        break;
                }
                tr.push("<td>" + json[i]["id"] + "</td>");
                tr.push("<td>" + json[i]["title"] + "</td>");
                tr.push("<td>" + begin + "</td>");
                tr.push("<td>" + end + "</td>");
                tr.push("<td>" + status + "</td>");
                tr.push("<td><button type='button' onclick='modify(" + json[i]["id"] + ")' class='btn btn-primary'>Modify</button></a></td>");
                tr.push("<td><button type='button' onclick='my_delete(" + json[i]["id"] + ")' class='btn btn-danger'>Delete</button></a></td>");
                tr.push('</tr>');
            }
            $('#mytable').append($(tr.join('')));
        });
});
function signout() {
    $.ajax({
            type: 'POST',
            url: '/signout'
        })
        .done(function(data, text_status, xhr) {
            if (xhr.status == 200)
                window.location.href = "/";
        });
}
function my_delete(id_delete) {
    $.ajax({
            type: 'POST',
            url: '/user/task/del/' + id_delete
        })
        .done(function(data, text_status, xhr) {
            if (xhr.status == 200)
                document.location.reload(true)
        });
    event.preventDefault();
}
$('.form_datetime').datetimepicker({
    weekStart: 1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight: 1,
    startView: 2,
    forceParse: 0,
    showMeridian: 0,
});