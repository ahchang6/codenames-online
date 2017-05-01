



var cssDebug = false;

//returns the color opposite of input
function oppositeColor(color){
	if(color == "Red"){
		return "Blue";
	}
	else if(color == "Blue"){
		return "Red";
	}
	return "Neutral";
}

//Function to change all the box on page to correspond to the words received from server
function changeWords(input){
	for(var x = 0; x<5;x++){
		for(var y = 0; y<5; y++){
			var index = 5*x+y+1;
			$("#click"+parseInt(index)+ " div").text(input[index-1]);

		}


	}

}

//Function to change all the box to the correct revealed color
function changeColor(input, isCodeMaster){
	for(var x = 0; x<5;x++){
		for(var y = 0; y<5; y++){
			var index = 5*x+y+1;
			var indexInString = "(" + x.toString() + ", " + y.toString() + ")";
			var valueOfPosition = input[indexInString];
			var colorString = "NONE";
			if (valueOfPosition.indexOf("False") >= 0 && !isCodeMaster){
				continue;
			}
			if (valueOfPosition.indexOf("BLUE") >= 0){
				colorString = "Blue";
			}
			else if (valueOfPosition.indexOf("RED") >= 0){
				colorString = "Red";
			}
			else if (valueOfPosition.indexOf("NEUTRAL") >= 0){
				colorString = "#ffc133";
			}
			if(!(colorString === "NONE")){
				$("#click"+parseInt(index)+ " div").css("background-color",colorString);
			}
		}

	}

}

$(document).ready(function() {

    


	var RedList = new Array();
	var BlueList = new Array();		


	if(cssDebug){
		return 0;

	}
	var request = {};
	// http://stackoverflow.com/questions/4209052/how-to-read-get-request-using-javascript
	var pairs = location.search.substring(1).split('&');
	for (var i = 0; i < pairs.length; i++) {
		var pair = pairs[i].split('=');
		request[pair[0]] = pair[1];
	}

	// remove all div with class "non-cm"
	if(request['player']=="cm"){	
	$(".non-cm").remove();
	}



	// requests and changes words
	$.ajax({
		url: "http://127.0.0.1:5000/get_words/" + request['room_id'],
		type: "GET",
		success: function(response){
			changeWords(response);
		},
		error: function(response,status,xhr){
			alert(status);
			alert("fail");

		},
	});

	//variable to check if we ever need to update
	var masterResponse = null;
	
	$.ajax({
		url: "http://127.0.0.1:5000/get_master_info/" + request['room_id'],
		type: "GET",
		success: function(response){
			masterResponse = response
				// checks to see if the player is Codemaster, revealing everything if it is
				var isCodeMaster = request['player'] === 'cm';
			changeColor(response, isCodeMaster);
			$('#overlay').remove();
		},
		error: function(response,status,xhr){
			alert(status);
			alert("fail");

		},
	});


	//updates the lists of words to the right
	function updateList(){
	$.ajax({
		url: "http://127.0.0.1:5000/get_team_words/" + request['room_id'] + "/Red",
		type: "GET",
		success: function(response){
			for(var i = 0;i<response.length;i++){
				if($.inArray(response[i],RedList)==-1){				
				$('<li class="removeable"><a href="#">' + response[i] + '</a></li>').appendTo("#red-list");
				RedList.push(response[i]);
				console.log(RedList);
				
				}
			}
		},
		error: function(response,status,xhr){
			alert(status);
			alert("fail");

		},
	});

	
	$.ajax({
		url: "http://127.0.0.1:5000/get_team_words/" + request['room_id'] + "/Blue",
		type: "GET",
		success: function(response){
			for(var i = 0;i<response.length;i++){			
				if($.inArray(response[i],BlueList)==-1){		
				$('<li class="removeable"><a href="#">' + response[i] + '</a></li>').appendTo("#blue-list");
				BlueList.push(response[i]);
				console.log(BlueList);
				}
			}
		},
		error: function(response,status,xhr){
			alert(status);
			alert("fail");

		},
	});



	}



	//live update function
	function updatePage(){
		$.ajax({
			url: "http://127.0.0.1:5000/get_master_info/" + request['room_id'],
			type: 'GET',
			success: function(response){
				updateList();
				//checks if we need to update by comparing if they are the same
				if(response == masterResponse){
				}
				else{
					changeColor(response,false);
					masterResponse=response;

				}
			}
		});
		
		$.ajax({
			url: "http://127.0.0.1:5000/get_info/" + request['room_id'],
			type: 'GET',
			success: function(response){
				//checks if we need to update by comparing if they are the same
					$('#team-turn').text(response[0]);
					$('#current-word').text(response[1]);
					$('#current-value').text(response[2]);

				setTimeout(updatePage,5000);
			}
		});

		
	}



	//calls live update function
	updatePage();

	
	






	//The buttons change color (or doesn't) depending on the status of the game
	$("[id*=click]").click(function(){

		var parsedInt = parseInt($(this).attr("id").substring(5));

		console.log(parsedInt);
		var y = (parsedInt - 1) % 5;
		var x = (parsedInt - y - 1) / 5;
		console.log(x);
		console.log(y);
		var item = this;
		$.ajax({
			url: "http://127.0.0.1:5000/play_move/" + request['room_id'] + "/" + request['player'] + "/" + x.toString() + "/" + y.toString(),
			type: "POST",
			success: function(response){
				if(response == "Go Again"){
					console.log("first");
					console.log($(item).attr('id'));
					$(item).find("div").css("background-color",request['player']);
				}
				else if(response == "Hit Neutral"){
					console.log("second");
					console.log($(item).attr('id'));
					$(item).find("div").css("background-color","#ffc133");
					$('#team-turn').text(oppositeColor($('#team-turn').text()));
				}
				else if(response == "Switch Turn"){
					console.log("third");
					console.log($(item).attr('id'));
					$(item).find("div").css("background-color",oppositeColor(request['player']));
					$('#team-turn').text(oppositeColor($('#team-turn').text()));
				}
				else if(response == "ASSASSIN"){
					console.log("fourth");
					console.log($(item).attr('id'));
					$(item).find("div").css("background-color","Black");
				}
				else{
				}
				$('#overlay').remove();
			},
			error: function(response,status,xhr){
				alert(status);
				alert("fail");

			},
		});

		


	});
	//passes turn when pressed if belongs to the current turn's team
	$("#pass-turn").click(function(event){
	$.ajax({
			url: "http://127.0.0.1:5000/pass_turn/" + request['room_id'] + "/" + request['player'],
			type: "POST",
			success: function(response){
				alert(response);
			},
			error: function(response,status,xhr){
				alert(status);
				alert("fail");

			},
		});



	});

	
	//places the word submittion for code master

	$('#team-placement').text(request['player']);
	if(request['player'] == 'cm'){
		$('#button-page').prepend('<form id="myform"><input type="text" size="30" value="Word" id="word"><input type="text" size="10" value="Guess Number" id="number"><button onclick="return buttonClick();">Submit</button></form>');
	}






});
//handles the action of the submittion of the word for the codemasters
function buttonClick(){
	var request = {};
	// http://stackoverflow.com/questions/4209052/how-to-read-get-request-using-javascript
	var pairs = location.search.substring(1).split('&');
	for (var i = 0; i < pairs.length; i++) {
		var pair = pairs[i].split('=');
		request[pair[0]] = pair[1];
	}

	var word = $('#word').val();
	var guessNum = $('#number').val();
	$.ajax({
		url: "http://127.0.0.1:5000/submit_word/" + request['room_id'] +"/" + word + "/" + guessNum,
		type: "POST",
		success: function(response){
		},
		error: function(response,status,xhr){
			alert(status);
			alert("fail");

		},
	});
	return false;
	
		
}

