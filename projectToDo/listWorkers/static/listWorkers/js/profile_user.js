$(document).ready(function(){

    $("#createButtonteam").click(function() {
        var serializedData =
        $("#createNewTeam").serialize();

        $.ajax({
            url: $("createNewTeam").data('url'),
            data: serializedData,
            type: 'post',
            success: function(response) {
                $("#yourteam").append('<p><img id="teams2" src="/static/listWorkers/img/teams2.png"><a id="yourteam" href="{% url 'list_workers' item.id %}">{{item.name_team}} </a></p>')
            }

        })

        $("#createNewTaskForm")[0].reset();

    });
});
