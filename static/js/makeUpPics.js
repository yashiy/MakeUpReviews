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

	$(".pin").click(function() {

		$('#enlarge-pic-id').attr('src', $(this).children('img').attr("src"));
		$('.enlarge-caption-text').text($(this).children('.caption').text());
		$('.enlarge-brand').text($(this).children('.brand').text());
		$('.enlarge-category').text($(this).children('.category').text());
		//$('.enlarge-stars').attr('class', $(this).children('div').attr("class"));
		$('#enlarge-pic').modal('show');
	})
	
	$(".pin").hover(function(){

		$(this).children(".thumbs").removeClass("hidden");
	}, function(){
		$(this).children(".thumbs").addClass("hidden");
	}
	)
	
/*	$(".star").hover(function(){
		console.log(this);
		var index = $('.star').index(this);
		for(var i =0;i <= index; i++){
			$('#star'+(i+1)).removeClass("glyphicon-star-empty");
			$('#star'+(i+1)).addClass("glyphicon-star");
		}
	}, function(){
		$('.star').removeClass("glyphicon-star");
		$('.star').addClass("glyphicon-star-empty");
	
	}); */	
	
	
	
	
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

}





$(document).ready(function() {
	rh.wp.enableButtons();
	rh.wp.attachEventHandler();
});