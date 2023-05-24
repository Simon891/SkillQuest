jobbT = ''

// Update inner HTML of div with ID "info"
function updateInfoDiv(retur, antal) {
  const infoDiv = document.getElementById('info_text');
  const infoDivAntal = document.getElementById('info_antal');
  const orginal = "Baserat på antal-n/a jobbannonser från 2022, så är följande de mest relevanta meningarna för jobbT-n/a:<br><br>";
  
  infoDiv.innerHTML = retur;
  infoDivAntal.innerHTML = orginal;
  infoDivAntal.innerHTML = infoDivAntal.innerHTML.replace('antal-n/a', antal);
  infoDivAntal.innerHTML = infoDivAntal.innerHTML.replace('jobbT-n/a', jobbT);
}

  
  // Send selected HTML back to Flask
  function sendSelectedHTML(selectedHTML) {
    document.getElementById("laddar").style.display="block";
    document.getElementById("laddar_img").style.display="block";
    fetch('/send_selected', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ selected_html: selectedHTML }),
    })
      .then(response => response.json())
      .then(data => {
        //console.log(data.retur, data.antal);
        updateInfoDiv(data.retur, data.antal);
        document.getElementById("laddar").style.display="none";
        document.getElementById("laddar_img").style.display="none";
        document.getElementById("info").style.display="block";

        const infoDiv = document.getElementById('info');
        const infoTextDiv = document.getElementById('info_text');
        const infoBannerDiv = document.getElementById('info_banner');
        const infoAntalDiv = document.getElementById('info_antal');
        const infoStangDiv = document.getElementById('info_stang');
        const infoSokAmsDiv = document.getElementById('sok_ams');
        infoDiv.style.height = 'auto';
        const contentHeight = infoTextDiv.offsetHeight + infoBannerDiv.offsetHeight + infoAntalDiv.offsetHeight + infoStangDiv.offsetHeight + infoSokAmsDiv.offsetHeight;
        infoDiv.style.height = contentHeight + 'px';

        
        setTimeout(() => {
          document.getElementById("info").classList.add('show');
          document.getElementById("forslag_ruta").style.height="0px";
        }, 100); // Delay of 100 milliseconds
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
        jobbT = selectedHTML;
        console.log('Clicked:', selectedHTML);
        sendSelectedHTML(selectedHTML);
      });
    });

    // Add an event listener to the div
    document.getElementById('info_stang').addEventListener('click', function() {
      sok_hight();
      document.getElementById("info").classList.remove('show');
      setTimeout(() => {
        document.getElementById("info").style.display="none";
      }, 1000);
    });
  });

  document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('myForm');
    form.addEventListener('submit', function(event) {
      document.getElementById('laddar').style.display = 'block';
      document.getElementById('laddar_img').style.display = 'block';
    });
  });
  
  function sok_hight() {
    const infoDiv = document.getElementById('forslag_ruta');
    const infoTextDiv = document.getElementById('resultat');
    const formDiv = document.getElementById('myForm');
    
    if (infoTextDiv.innerHTML.trim() !== '') {
      infoTextDiv.style.visibility = 'hidden';
      infoTextDiv.style.height = 'auto';
      const contentHeight = infoTextDiv.offsetHeight + formDiv.offsetHeight;
      infoTextDiv.style.visibility = 'visible';
      infoDiv.style.height = contentHeight + 'px';
  
      if (contentHeight > window.innerHeight) {
        infoDiv.style.top = '0';
        infoDiv.style.bottom = '';
      }
    }
  }
  
  document.addEventListener('DOMContentLoaded', function() {
    setTimeout(sok_hight, 500);
  });
  
  document.addEventListener("DOMContentLoaded", function() {
    var sokAmsElement = document.getElementById("sok_ams");
    sokAmsElement.addEventListener("click", function() {
      var address = "https://arbetsformedlingen.se/platsbanken/annonser?q="+jobbT;
      window.open(address, "_blank");
    });
  });
