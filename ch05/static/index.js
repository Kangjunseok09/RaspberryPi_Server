var setNew = document.querySelector('#Now')
var setRecord = document.querySelector('#Record')

setNew.addEventListener("click", function () {
    $.ajax({
        type: 'GET',
        url: '/now'
    }).done(function (result) {
        console.log(result)
        var tdata = "<tr>"
        tdata += "<td>now</td>"
        tdata += "<td>now</td>"
        tdata += "<td>" + result[1] + "*C</td>"
        tdata += "<td>" + result[0] + "%</td>"
        tdata += "</tr>"
        document.getElementById("table").innerHTML = tdata
    }).fail(function (result) {
        console.log(result)
    })
});

setRecord.addEventListener("click", function () {
    $.ajax({
        type: 'GET',
        url: '/record'
    }).done(function (result) {
        console.log(result)
        var tabledata = ""
        for (var i in result) {
            var data = result[i]
            tabledata += "<tr>"
            tabledata += "<td>" + data[0] + "</td>"
            tabledata += "<td>" + data[3] + "</td>"
            tabledata += "<td>" + data[2] + "*C</td>"
            tabledata += "<td>" + data[1] + "%</td>"
            tabledata += "</tr>"
        }
        document.getElementById("table").innerHTML = tabledata
    }).fail(function (result) {
        console.log(result)
    })
});

