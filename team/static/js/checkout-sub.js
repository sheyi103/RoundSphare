const stripe = Stripe("pk_test_9TplBiLCjfeQmzwgYJpQx76D00chCsKzI5");

initialize();

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
// Create a Checkout Session
async function initialize() {
  var csrftoken = getCookie('csrftoken');
  console.log("crs...",csrftoken)
  const fetchClientSecret = async () => {
    const response = await fetch("/checkout", {
      method: "POST",
      'X-CSRFToken': 'AsraaF9vrnoNDqr0107uVGIbsYmCZJsZ'
    });
    const { clientSecret } = await response.json();
    return clientSecret;
  };

  const checkout = await stripe.initEmbeddedCheckout({
    fetchClientSecret
  });

  console.log("........")
  // Mount Checkout
  checkout.mount('#checkout');
}
