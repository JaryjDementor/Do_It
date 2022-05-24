$(document).ready(function(){
    var csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    $("#createButton").click(function() {
        var serializedData =
        $("#createNewTaskForm").serialize();

        $.ajax({
            url: $("createNewTaskForm").data('url'),
            data: serializedData,
            type: 'post',
            success: function(response) {
                $("#taskList").append('<div class="card mb-1" id="taskCard" data-id="' + response.task.id + '"><div class="card-body">' + 'Discription: ' + response.task.description + '<br>' + 'Status: ' + response.task.status + '<br>' + 'Categories: ' + response.task.categories + '<br>' + 'Date of completion: ' + response.task.date_of_completion + '<br>' + '<button type="button" class="close float-right" data-id="' + response.task.id + '"><span aria-hidden="true">&times;</span></button></div></div>')
            }

        })

        $("#createNewTaskForm")[0].reset();

    });

    $("#taskList").on('click', '.card', function() {
        var dataId = $(this).data('id');

        $.ajax({
            url: '/tasks/' + dataId + '/completed/',
            data: {
                csrfmiddlewaretoken: csrfToken,
                id: dataId
            },
            type: 'post',
            success: function() {
                var cardItem = $('#taskCard[data-id="' + dataId + '"]');
                cardItem.css('text-decoration', 'line-through').hide().slideDown();
                $("#taskList").append(cardItem);
            }
        });
    }).on('click', 'button.close', function(event) {
        event.stopPropagation();

        var dataId = $(this).data('id');

        $.ajax({
            url: '/tasks/' + dataId + '/delete/',
            data: {
                csrfmiddlewaretoken: csrfToken,
                id: dataId
            },
            type: 'post',
            dataType: 'json',
            success: function() {
                $('#taskCard[data-id="' + dataId + '"]').remove();
            }
        })
    });
});

