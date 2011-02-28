function applyLineCommentMakers(line, comment) {
  // Add a border to a commented line
  $(line).addClass('line-with-comment');

  // Add an onclick to the line to show it's comment
  $('#' + comment + '-icon').click(function(){
    $('#' + comment).clone().dialog({width:500});
    return false;
  });

  // Add a little icon to further illustrate the comment is present
  var offset = $(line).offset()
  var width = $(line).width()
  var line_top = 0;
  var line_left = 0;

  // Calculate offsets
  if (offset.left < 50) {
    line_left = offset.left + width + 5;
  } else {
    line_left = offset.left - 24;
  }

  // Move the icon into place
  $('#' + comment + '-icon').css(
    {'position':'absolute',
     'left':line_left,
     'top':offset.top - 20
    }
  ).show();
}

function enableCodeComments(selector, diffIndex) {
  $(selector).selectable({
    distance: 20,
    stop: function () {
      var line_numbers = [];
      var lines = [];
      var msg = [];
      var hash;

      // Extract the properites of the selected lines of code
      $(selector + ' .ui-selected').each(function() {
        line_numbers.push($(selector + ' pre').index(this));
        lines.push(this);
        msg.push(this.innerHTML);
      })

      // Add a tip into the message?
      msg.push('', 'Your comment here...');

      // Calculate a hash based on the lines being commented on
      hash = 'msg' + diffIndex + line_numbers.join('')

      // Create a div to hold the preformatted message
      var textarea = document.createElement('textarea');
      textarea.setAttribute('id', hash);
      textarea.innerHTML = msg.join('\n');
      $('body').append(textarea);
      $('#' + hash).dialog({
        height:300,
        width:600,
        buttons: {
          'Cancel':function() {
            $(this).dialog('close');
          },
          'Save comment':function() {
            url = '/api/comment/persist'
            args = {
              'diff_index':diffIndex,
              'line_numbers':line_numbers.join(','),
              'msg':this.value,
              'r':$('#r').val()
            };

            $.post(url, args, function(data, status, xhr) {
                console.log(data);
                console.log(status);

                // Leave a marker (span) to pull up the msg later
                var span = document.createElement('span');
                span.setAttribute('id', hash + '-icon');
                span.setAttribute('class', 'comment-icon hidden');

                // Add a label with the comment count to the span
                var label = document.createElement('label');
                label.innerHTML = '1';
                span.appendChild(label);

                // Add the message to the dom
                $('body').append(span);

                // Try to flag the line and add a notification callout
                applyLineCommentMakers(lines[0], hash);
            })

            // Close the dialog after
            $(this).dialog('close');

          }
        }
      }).width('100%');

      // Reset the css so it's not selected looking
      $.each(lines, function(index, value) {
        $(value).removeClass('ui-selected');
      });

    }
  });
}

// Enable code comments when the dom is ready
$(document).ready(function () {
  enableCodeComments('#diff0 .after', 0);
  enableCodeComments('#diff1 .after', 1);
});
