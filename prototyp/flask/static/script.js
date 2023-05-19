// Update inner HTML of div with ID "info"
function updateInfoDiv(html) {
    const infoDiv = document.getElementById('info');
    infoDiv.innerHTML = html;
  }
  
  // Send selected HTML back to Flask
  function sendSelectedHTML(selectedHTML) {
    fetch('/send_selected', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ selected_html: selectedHTML }),
    })
      .then(response => response.json())
      .then(data => {
        console.log(data.selected_html);
        updateInfoDiv(data.selected_html);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
  
  // Attach click event listener to suggestion divs
  document.addEventListener('DOMContentLoaded', function() {
    const suggestionDivs = document.getElementsByClassName('forslag');
    Array.from(suggestionDivs).forEach(div => {
      div.addEventListener('click', function() {
        const selectedHTML = this.innerHTML;
        console.log('Clicked:', selectedHTML);
        sendSelectedHTML(selectedHTML);
      });
    });
  });
  