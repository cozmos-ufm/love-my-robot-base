$(document).ready(function() {
    $('.execute').click(function(){
        $.get('/send', function(data, status) {
            console.log(`${data.message} and status is ${status}`)
            alert(data.message)
            setTimeout(function() {
                location.reload();
            }, 0);
        })
    })
    $('.clear').click(function(){
        $.get('/clear', function(data, status) {
            console.log(`${data.message} and status is ${status}`)
            alert(data.message)
            setTimeout(function() {
                location.reload();
            }, 0);
        })
    })
    $('.par').click(function() {
        console.log("hola")
        let id = $(this).text()
        $('#inputGroup-sizing-lg').html(id)
        console.log($('#inputGroup-sizing-lg').text());
    })
    $('.nopar').click(function() {
        console.log("hola")
        let id = $(this).text()
        $.post('/save-code', {name:id}, function(data, status) {
            console.log(`${data.message} and status is ${status}`)
            alert(data.message)
            setTimeout(function() {
                location.reload();
            }, 0);
        })
        console.log(id);
    })
    $('.li1').click(function() {
        console.log("hola")
        let id = $(this).attr('id')
        console.log(id);
        if (id && id.length > 0) {
            $.post('/delete-code', {id:id}, function(data, status) {
                console.log(`${data.message} and status is ${status}`)
                alert(data.message)
                setTimeout(function() {
                    location.reload();
                }, 0);
            })
        }
    })
    $('.send').click(function() {
        let newName = $('#nombre').val()
        console.log(newName);
        if (newName && newName.length > 0) {
            $.post('/save-code', {name:newName}, function(data, status) {
                console.log(`${data.message} and status is ${status}`)
                alert(data.message)
                setTimeout(function() {
                    location.reload();
                }, 0);
            })
        }
    })
    $('#save').click(function() {
        let code = $('#inputGroup-sizing-lg').text()
        let params = $('#inputcode').val()
        let line = code + " " +params
        console.log(line);
        if (line && line.length > 0) {
            $.post('/save-code', {name:line}, function(data, status) {
                console.log(`${data.message} and status is ${status}`)
                alert(data.message)
                setTimeout(function() {
                    location.reload();
                }, 0);
            })
        }
    })
})
