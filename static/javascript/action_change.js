function	visibility(state) {
	if (!state)
	{
		$('#id_genre').parent().hide();
		$('#id_name').parent().hide();
		$('#id_auteur').parent().hide();
		$('#id_commentaire').parent().hide();
		$('#id_fichier').parent().hide();
	}else
	{
		$('#id_genre').parent().show();
		$('#id_name').parent().show();
		$('#id_auteur').parent().show();
		$('#id_commentaire').parent().show();
		$('#id_fichier').parent().show();
	}
}

$(document).ready(function() {
	if ($('#id_matiere').val() == "")
	{
		$('#id_matiere').parent().hide();
		visibility(false);
	}
	if ($('#id_sous_matiere').val() == "")
		$('#id_sous_matiere').parent().hide();
});

function	change(string, mod, action_type, foo)
{
	$.ajax({
		"type" : "GET",
		"url" : "/thuysses/action_change/?" + string + "=" + action_type,
		"dataType" : "json",
		"cache" : false,
		"success" : function(json) {
			$('#id_' + mod + ' >option').remove();
			for(var j = 0; j < json.length; j++) {
				$('#id_' + mod).append($('<option></option>').val(json[j][0]).html(json[j][1]));
			}
			if ($('#id_' + mod + ' >option').length > 1)
				$('#id_' + mod).parent().show();
			else
				$('#id_' + mod).parent().hide();
			foo();
		}
	});
}

function	annee_change()
{
	var action_type = $('#id_annee').val();
	change("annee", "matiere", action_type, function() {
		if ($('#id_matiere >option').length == 0 || $('#id_matiere').val() == "")
		{
			visibility(false);
			$('#id_sous_matiere').parent().hide();
		}
		});
}

function	matiere_change()
{
	var action_type = $('#id_matiere').val();
	change("matiere", "sous_matiere", action_type, function() {
		if ($('#id_sous_matiere >option').length == 0)
			visibility(true);
		else
			visibility(false);
		if (action_type == "")
			visibility(false);
		});
}

function	sous_matiere_change()
{
	if ($('#id_sous_matiere >option').length > 0)
		visibility(true);
	else
		visibility(false);
	if ($('#id_sous_matiere').val() == "")
		visibility(false);
}
