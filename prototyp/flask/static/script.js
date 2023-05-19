// Send selected HTML back to Flask
function sendSelectedHTML(selectedHTML) {
    console.log('Selected HTML:', selectedHTML); // Log the selected HTML to the console
    
    fetch('/send_selected', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ selected_html: selectedHTML }),
    })
      .then(response => response.json())
      .then(data => {
        console.log(data.message); // Log the response data to the console
      })
      .catch(error => {
        console.error('Error:', error); // Log any errors to the console
      });
  }
  

  document.addEventListener('DOMContentLoaded', function() {
    // Attach click event listener to suggestion divs
    const suggestionDivs = document.getElementsByClassName('forslag');
    Array.from(suggestionDivs).forEach(div => {
      div.addEventListener('click', function() {
        const selectedHTML = this.innerHTML;
        console.log('Clicked:', selectedHTML);
        sendSelectedHTML(selectedHTML);
      });
    });
  });
  