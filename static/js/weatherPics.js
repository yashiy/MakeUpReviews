var rh = rh || {};
rh.wp = rh.wp || {};

rh.wp.editing = false;

rh.wp.attachEventHandler = function(){
	$("#insert-pic-modal").on('shown.bs.modal', function(){
		$("input[name=image_url]").focus();
	});
}

rh.wp.enableButtons = function(){

	$("#toggle-edit").click(function(){
		if(rh.wp.editing){
			rh.wp.editing = false;
			$(".edit-actions").addClass("hidden");
			$(this).html("Edit");
		}else{
			rh.wp.editing = true;
			$(".edit-actions").removeClass("hidden");
			$(this).html("Done");
		}
	});
	
	$("#add-pic").click(function(){
		$("#insert-pic-modal .modal-title").html("Add a Weather Pic");
		$("#insert-pic-modal button[type=submit]").html("Add Weather Pic");
	
		$("#insert-pic-modal input[name=image_url]").val("");
		$("#insert-pic-modal input[name=caption]").val("");
		$("#insert-pic-modal input[name=entity_key]").val("").prop("disabled", true);

	});
	
	$(".edit-pics").click(function(){
		$("#insert-pic-modal .modal-title").html("Edit this Weather Pic");
		$("#insert-pic-modal button[type=submit]").html("Edit Weather Pic");			
	
		image_url = $(this).find(".image_url").html();
		caption = $(this).find(".caption").html();
		entity_key = $(this).find(".entity_key").html();
		$("#insert-pic-modal input[name=image_url]").val(image_url);
		$("#insert-pic-modal input[name=caption]").val(caption);
		$("#insert-pic-modal input[name=entity_key]").val(entity_key).prop("disabled", false);

	});
}

$(document).ready(function(){
	rh.wp.enableButtons();
	rh.wp.attachEventHandler();
});
//$("#toggle-edit").click(function(){
//	$(".edit-actions").toggleClass("hidden")
//});