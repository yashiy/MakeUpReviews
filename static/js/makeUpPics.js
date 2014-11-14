var rh = rh || {};
rh.wp = rh.wp || {};

rh.wp.editing = false;
rh.wp.test = -1;

rh.wp.attachEventHandler = function() {
	$("#insert-pic-modal").on('shown.bs.modal', function() {
		$("input[name=image_url]").focus();
	});
}

rh.wp.enableButtons = function() {

	$("#toggle-edit").click(function() {
		if (rh.wp.editing) {
			rh.wp.editing = false;
			$(".edit-actions").addClass("hidden");
			$(this).html("Edit");
		} else {
			rh.wp.editing = true;
			$(".edit-actions").removeClass("hidden");
			$(this).html("Done");
		}
	});

	$("#add-pic").click(
			function() {
				$("#insert-pic-modal .modal-title").html("Add a Makeup Pic");
				$("#insert-pic-modal button[type=submit]").html(
						"Add Makeup Pic");

				$("#insert-pic-modal input[name=image_url]").val("");
				$("#insert-pic-modal input[name=caption]").val("");
				$("#insert-pic-modal input[name=entity_key]").val("").prop(
						"disabled", true);
				$('.star').removeClass("glyphicon-star");
				$('.star').addClass("glyphicon-star-empty");

			});

	$(".edit-pics").click(
			function() {
				$("#insert-pic-modal .modal-title")
						.html("Edit this Makeup Pic");
				$("#insert-pic-modal button[type=submit]").html(
						"Edit Makeup Pic");

				image_url = $(this).find(".image_url").html();
				caption = $(this).find(".caption").html();
				entity_key = $(this).find(".entity_key").html();
				$("#insert-pic-modal input[name=image_url]").val(image_url);
				$("#insert-pic-modal input[name=caption]").val(caption);
				$("#insert-pic-modal input[name=entity_key]").val(entity_key)
						.prop("disabled", false);

			});

	$(".pin").children().not(".thumbs").click(function() {
		
			for(i = 1; i <= 5; i++) {
				$("#en-star" + i).addClass("glyphicon-star-empty");
				$("#en-star" + i).removeClass("glyphicon-star");
			}
		
		
			$('#enlarge-pic-id').attr('src', $(this).parent('.pin').children('img').attr("src"));
			$('.enlarge-caption-text').text( $(this).parent('.pin').children('.caption').text());
			$('.enlarge-brand').text( $(this).parent('.pin').children('.brand').text());
			$('.enlarge-category').text( $(this).parent('.pin').children('.category').text());
			//$('.enlarge-stars').attr('class', $(this).children('div').attr("class"));
			$('#enlarge-pic').modal('show');
			
			console.log($(".en_star_rating_class").text())
			
			for (i = 1; i <= parseInt($(this).parent('.pin').children(".en_star_rating_class").val(), 10); i++) {
				$("#en-star" + i).removeClass("glyphicon-star-empty");
				$("#en-star" + i).addClass("glyphicon-star");
			}
			
			
	})
	
	$(".pin").hover(function(){

		$(this).children(".thumbs").fadeIn();
	}, function(){
		$(this).children(".thumbs").fadeOut();
	}
	)
	
	
	$(".star").hover(function(){
			var index = $('.star').index(this);
			for(var i =0;i <= index; i++){
				$('#star'+(i+1)).removeClass("glyphicon-star-empty");
				$('#star'+(i+1)).addClass("glyphicon-star");
			}
	}, function(){
		if(rh.wp.test == -1){ // a click has not occurred
			$('.star').removeClass("glyphicon-star");
			$('.star').addClass("glyphicon-star-empty");
		}else{ // a click had occurred 
			$('.star').removeClass("glyphicon-star");
			$('.star').addClass("glyphicon-star-empty");
			for(var i =0;i <= rh.wp.test; i++){
				$('#star'+(i+1)).removeClass("glyphicon-star-empty");
				$('#star'+(i+1)).addClass("glyphicon-star");
			}
		}
	});
	
	$(".star").click(function(){
		rh.wp.test = $('.star').index(this);
		var index = $('.star').index(this);
		console.log(index);
		$('.star').removeClass("glyphicon-star");
		$('.star').addClass("glyphicon-star-empty");
		for(var i =0;i <= index; i++){
			$('#star'+(i+1)).removeClass("glyphicon-star-empty");
			$('#star'+(i+1)).addClass("glyphicon-star");
		}
		$('#star-number').val(index+1);
	});
	
	
	var updateProgressBar = function(thumbPressed) {
		var agreeValue = parseInt($(thumbPressed).parent().parent().children(".thumbs").children('.addAgree').text(), 10);
		var disagreeValue = parseInt($(thumbPressed).parent().parent().children(".thumbs").children('.addDisagree').text(), 10);

		var agreeInt = parseInt(agreeValue, 10);
		var disagreeInt = parseInt(disagreeValue, 10);
		
		var agreeProgress = (agreeInt / (agreeInt + disagreeInt)) * 100;
		var disagreeProgress = (disagreeInt / (agreeInt + disagreeInt)) * 100;
		
		
		console.log($(thumbPressed).parent().parent().children(".progress").children(".agree-bar"))
		
		$(thumbPressed).parent().parent().children(".progress").children(".agree-bar").css("width", agreeProgress + "%");
		$(thumbPressed).parent().parent().children(".progress").children(".disagree-bar").css("width", disagreeProgress + "%");
		
	}
	
	
	$(".thumb-up").click(function() {
		//$(this).parent().parent().children('.addAgree').text(agreeValue + 1);		$("#agree-number").val(agreeValue + 1);	
		var data =  {"agree": "true", "disagree":"false",
				"makeup_key": $(this).parent().children('.makeup_key').val()};
		var thumbup = this
		$.ajax({
			method:"POST",
			url:"/likesupdate",
			data:data,
			success: function(res){
				res = JSON.parse(res);
				$(thumbup).parent().parent().children(".thumbs").children('.addAgree').html(res.agree);
				$(thumbup).parent().parent().children(".thumbs").children('.addDisagree').html(res.disagree);
				
				
			},
			error: function(err){
				
			}		
		})
		
		updateProgressBar(this);	
		
	});
	
	$(".thumb-down").click(function() {
		//$(this).parent().parent().children('.addAgree').text(agreeValue + 1);		$("#agree-number").val(agreeValue + 1);	
		var data =  {"agree": "false", "disagree":"true",
				"makeup_key": $(this).parent().children('.makeup_key').val()};
		var thumbup = this
		$.ajax({
			method:"POST",
			url:"/likesupdate",
			data:data,
			success: function(res){
				res = JSON.parse(res);
				$(thumbup).parent().parent().children(".thumbs").children('.addAgree').html(res.agree);
				$(thumbup).parent().parent().children(".thumbs").children('.addDisagree').html(res.disagree);
			},
			error: function(err){
				
			}
		})
		updateProgressBar(this);	

	});
	
	
	$("#localpic").click(function() {
		console.log("local pic clicked!");
		$(".fileinput").removeClass("hidden");
		$(".fileinput").fadeIn();
		
		$(".upload-from-web").addClass("hidden");
		$(".upload-from-web").fadeOut();
	})
	
	$("#webpic").click(function() {
		console.log("web pic clicked!");
		$(".upload-from-web").removeClass("hidden");
		$(".upload-from-web").fadeIn();
		
		$(".fileinput").addClass("hidden");
		$(".fileinput").fadeOut();
	})

}


$(".sort").click(function(){
	if($(this).attr("id") == "sort-by-most-recent"){
		window.location = window.location.href.split("?")[0] + "?sortby=recent";
	}else{
		window.location = window.location.href.split("?")[0] + "?sortby=pop";
	}
	
})




$(document).ready(function() {
	rh.wp.enableButtons();
	rh.wp.attachEventHandler();
});