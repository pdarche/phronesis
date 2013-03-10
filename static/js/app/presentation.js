$( document ).ready( function(){

	$.ajax({
		url : '/static/js/templates/queryView.handlebars',
		method : 'GET',
		success: function(data) { 
			template = data

			console.log("doin it")

			var source = $(template).html()
		    var template = Handlebars.compile( source )
		    $('body').append( template )

		}
	})

	$('.attribute').click( function() {
		var attribute = $(this).attr('id')
	})

	$('.chart-button').click( function(){

		var selector = '#' + $(this).attr('id').split("_")[0]
		$(selector).removeClass().addClass('tall chart')
		$('.chart').not(selector).removeClass().addClass('short chart')

	})

	$('.chart-button').click(function(){
		$('.chart-button').removeClass('active')
		$(this).addClass('active')
	})

	$('.attribute').click(function(){
		$('.attribute').removeClass('active')
		$(this).addClass('active')
	})

	initialize(40.725324,-73.953931)

	var lineChart = new Highcharts.Chart( config )

	var template;

	$('#add_attribute').click( function(){
		$.ajax({
			url : '/static/js/templates/query.handlebars',
			method : 'GET',
			success: function(data) { 
				template = data

				var attr = $('ul').find('.active').attr('id')
				var attribute = d[attr]

				console.log(attribute)

				var source = $(template).html()
			    var template = Handlebars.compile( source )
			    $('#domain_attributes').append( template({ "attribute" : attribute }) )

			    $('.remove').click(function(){
					$(this).parent().remove()
				})

			}
		})
	})

	$('#go').click( function(){
		var personalAttr = $('ul').find('.active').attr('id')
			
			url = '/v1/data/pdarche/body/' + personalAttr

			if ( $('.query-options').length > 0 ) {

				url += '?'

				$.each($('.query-options'), function(i){

					var objAttr = $('.query-options').eq(i).find('.obj_attr:selected').val(),
						filter = $('.query-options').eq(i).find('.query_filter:selected').val(),
						val = $('.query-options').eq(i).find('#query_text').val()
					
					if (i === 0){

						url += objAttr + "__" + filter + "=" + val

					} else {

						url += "&" + objAttr + "__" + filter + "=" + val
					}

				})

				if ( $('#button_container').find('.active').length < 1 ){
					alert("please select where you would like the data displayed")
				} else {

					$.getJSON(url, function(data){

						var target = $('#button_container').find('.active').attr('id').split('_')[0]

						if ( target === "map"){
							for (var i = 0; i < data.length; i++ ){

								var lon = data[i].loc[0],
									lat = data[i].loc[1]

								loc = new google.maps.LatLng(lat,lon);

								addMarker(loc)

							}

						} else {

							var series = []

							for ( var j = 0; j < data.length; j++ ){
								var unix = (data[j].created_at * 100),
									datum = data[j].steps,
									dataPoint = [unix, datum]

								series.push(dataPoint)
							}

							console.log(series)

					        lineChart.addSeries({
					             data: series,           
					        }, true);
							
						}

					})
				}
			}

	})

})

var d = {
	"sleep" : [
		"time_in_light", "total_z_zq_points", "time_to_z",
		"time_in_rem", "time_in_deep", "time_in_wake", 
		"total_z",
	],
	"nutrition" : [ "title"],
	"physicalActivity" : [
		"distance", "mins_sedentary", "steps",
		"mins_lightly_active", "mins_fairly_active",
		"mins_very_active", "floors", "calories_out"
	],
	"location" : [
		"source", "lat", "lon", "venue", 		
	]
}


var map;

function initialize(lat, lon) {
var myOptions = {
  zoom: 16,
  center: new google.maps.LatLng(lat,lon),
  mapTypeId: google.maps.MapTypeId.ROADMAP,

};
map = new google.maps.Map(document.getElementById('map'), myOptions);
testMarker(map) 
}

// Function for adding a marker to the page.
function addMarker(location) {
  marker = new google.maps.Marker({
      position: location,
      map: map
  });
}

// Testing the addMarker function
function testMarker() {
     myHouse = new google.maps.LatLng(40.725324,-73.953931);
     addMarker(myHouse);
}