document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('refresh-button').addEventListener('click', function() {
      window.location.href = '/plot/';
  });

  document.getElementById('delete-button').addEventListener('click', function() {
      if (confirm('Are you sure you want to delete the file?')) {
          fetch('/delete/', {
              method: 'POST',
              headers: {
                  'X-CSRFToken': getCookie('csrftoken'),
              }
          }).then(response => {
              if (response.ok) {
                  window.location.href = '/';
              } else {
                  alert('Failed to delete the file.');
              }
          });
      }
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
