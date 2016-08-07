$('.form').find('input, textarea').on('keyup blur focus', function (e) {
  
  var $this = $(this),
      label = $this.prev('label');

	  if (e.type === 'keyup') {
			if ($this.val() === '') {
          label.removeClass('active highlight');
        } else {
          label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight'); 
			} else {
		    label.removeClass('highlight');   
			}   
    } else if (e.type === 'focus') {
      
      if( $this.val() === '' ) {
    		label.removeClass('highlight'); 
			} 
      else if( $this.val() !== '' ) {
		    label.addClass('highlight');
			}
    }

});

$('.tab a').on('click', function (e) {
  
  e.preventDefault();
  
  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');
  
  target = $(this).attr('href');

  $('.tab-content > div').not(target).hide();
  
  $(target).fadeIn(600);
  
});

document.onkeydown = function(e) {
    e = e || window.event;

    if (e.keyCode == '38') {
        // up arrow
        $("#arrow_up").click();
        $("#arrow_up").css("border-bottom", "80px solid #ffffff");
    }
    else if (e.keyCode == '40') {
        // down arrow
        $("#arrow_down").click();
       $("#arrow_down").css("border-top", "80px solid #ffffff");
    }
}


document.onkeyup = function(e) {
    e = e || window.event;

    if (e.keyCode == '38') {
        // up arrow
        $("#arrow_up").css("border-bottom", "80px solid #1ab188");
    }
    else if (e.keyCode == '40') {
        // down arrow
        $("#arrow_down").css("border-top", "80px solid #1ab188");
    }
}