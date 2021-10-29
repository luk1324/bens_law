
    //Obtenemos la información de csfrtoken que se almacena por cookies en el cliente
    var csrftoken = getCookie('csrftoken');

    //Agregamos en la configuración de la funcion $.ajax de Jquery lo siguiente:
    $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                            // Send the token to same-origin, relative URLs only.
                            // Send the token only if the method warrants CSRF protection
                            // Using the CSRFToken value acquired earlier
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
    });

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

// usando jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function csrfSafeMethod(method) {
    // estos métodos no requieren CSRF
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
var graph_data = []
function draw(){
    if($('#benfords_data').length > 0){
        const value = JSON.parse(document.getElementById('benfords_data').textContent);
        if (!('first_number' in value)){
            for (var i=0; i<9; i++){
                graph_data.push([value[i].num, value[i].your, value[i].ben]);
            }

        }else{
            arr1 = value.first_number;
            arr2 = value.Benford;
            for (var i=1; i<10; i++){
                graph_data.push([i, parseFloat((arr1[i]*100).toFixed(1)), parseFloat((arr2[i]*100).toFixed(1))]);
            }
        }

        //count chi_square
        console.log(graph_data)
        var chi_square = 0;
        for (var i=0; i<9; i++){
            observed = graph_data[i][1]
            console.log(observed)
            expected = graph_data[i][2]
            console.log(expected)
            chi_square += chi_square + (Math.pow((observed-expected),2) / expected)
            console.log(chi_square)
        }
        chi_tagret = 15.51
        is_similar(chi_square, chi_tagret)
        
        google.charts.load('current', {packages: ['corechart', 'line']});
        google.charts.setOnLoadCallback(drawLineColors);
    }
}
draw();

function drawLineColors() {
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'X');
    data.addColumn('number', 'Your Data');
    data.addColumn('number', 'Benford Distribution');

    data.addRows(graph_data);

    var options = {
      hAxis: {
        title: 'Leading Number'
      },
      vAxis: {
        title: 'Percent'
      },
      colors: ['#a52714', '#097138']
    };

    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
    chart.draw(data, options);
  }


$(document).on('click', '.send_column', function(){
    var formData = new FormData();
    //var csrftoken = getCookie('csrftoken');
    formData.append('column', $(this).attr('value'));
    //formData.append('csrfmiddlewaretoken', csrftoken);
    $.ajax({
        type: 'POST',
        url: "ajax/postColumn",
        data: formData,
        async: true,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            if ('low' in response){
                content = '<div class="alert alert-danger" role="alert">Data must contain all leading numbers in range of 1 to 9</div>';
                $('.modal-body').empty().append(content);    
            }else{
                $("button[data-bs-dismiss='modal']").click()
                $('#to_replace').empty().append(response);
                draw();
            }
            
        },
        error: function (response) {
            console.log('error' + response.reponseText);
        }
    })    
        
});

$(document).on('click', 'tr.select_set', function(){
    var formData = new FormData();
    formData.append('set_id', $(this).children().eq(0).text());
    console.log($(this).children().eq(0).text());
    $.ajax({
        type: 'POST',
        url: "ajax/getSavedSet",
        data: formData,
        async: true,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            $('#to_replace').empty().append(response);
           draw();
        },
        error: function (response) {
            console.log('error' + response.reponseText);
        }
    })    
        
});

function is_similar(chi, target){
    content = '<div>ChiSquare = '+chi.toFixed(2)+' (Target = ' + target + ')<div><br>'
    
    if (chi<target){
        result = 'success'
        content += '<div>Your Data Set matches Benford`s Law</div>'
    }else{
        result = 'danger'
        content += '<div>Sorry, data don`t match Benford`s Law</div>'
    }

    wrap = '<div class="alert alert-'+ result +'" role="alert">'+ content+'</div>';
    $('.col-8').append(wrap);
}