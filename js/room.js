$(document).ready(function() {
	var request = {};
	// http://stackoverflow.com/questions/4209052/how-to-read-get-request-using-javascript
	var pairs = location.search.substring(1).split('&');
	for (var i = 0; i < pairs.length; i++) {
		var pair = pairs[i].split('=');
		request[pair[0]] = pair[1];
	}



	$("#codemaster-button").click(function(){

		$('#codemaster-button').attr('href','panel.html?room_id=' + request['room_id'] + '&player=cm' )

	});

	$("#blue-team-button").click(function(){

		$('#blue-team-button').attr('href','panel.html?room_id=' + request['room_id'] + '&player=Blue' )

	});

	$("#red-team-button").click(function(){

		$('#red-team-button').attr('href','panel.html?room_id=' + request['room_id'] + '&player=Red' )

	});


});
	
