
async function sendToGPT3(input) {
    const apiKey = config('OPENAI_API_KEY')
    const endpoint = 'https://api.openai.com/v1/completions?api_key=' + apiKey;
    const data = {
      model: "text-davinci-003",
      prompt: input,
      max_tokens: 100,
      temperature : 0
    };

    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${apiKey}`},
        body: JSON.stringify(data)
    };

    try {
      const response = await fetch(endpoint, options);
      const json = await response.json();
      return json.choices[0].text;
    } catch (err) {
          console.log("Error occured while fetching the data :",err)
          return "Sorry, there was an error processing your request. Please try again later.";
    }
    return json.choices[0].text;
    }


      const chatbotButton = document.querySelector("#chatbot-button");

      const chatbotWindow = document.querySelector("#chatbot-window");

      const closeButton = document.querySelector("#close-button");

      const chatbotMessages = document.querySelector("#chatbot-messages");

      const chatbotForm = document.querySelector("#chatbot-form");

      const messageInput = document.querySelector("#message-input");

      const sendButton = document.querySelector(".send-button");

      chatbotButton.addEventListener("click", () => {
        chatbotWindow.classList.toggle("open");
        chatbotButton.classList.toggle("open");
      });

      closeButton.addEventListener("click", () => {
        chatbotWindow.classList.remove("open");
      });


        chatbotForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const messageText = messageInput.value;
        var emptyMessageAlert = document.querySelector(".empty-message-alert");

        if (!messageText) {
          emptyMessageAlert.innerHTML = "Please enter your message";
          emptyMessageAlert.style.display = "block";
          document.querySelector(".message-input").classList.add("shake");
          return false;
        }
        
        emptyMessageAlert.style.display = "none";
        document.querySelector(".message-input").classList.remove("shake")
        messageInput.value = "";

        const messageElement = document.createElement("div");
        messageElement.classList.add("chatbot-message", "user");
        messageElement.innerText = messageText;
        chatbotMessages.appendChild(messageElement);

        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

        const typingElement = document.createElement("div");
        typingElement.classList.add("chatbot-message", "typing");
        typingElement.innerHTML = "<span class='typing-animation'></span><span class='typing-animation'></span><span class='typing-animation'></span>";
        chatbotMessages.appendChild(typingElement);

        setTimeout(async () => {
        chatbotMessages.removeChild(typingElement);

        const responseElement = document.createElement("div");
        responseElement.classList.add("chatbot-message", "bot");
        var input = messageText;
        console.log(input);

        const response = await sendToGPT3(input);
        console.log(response);

        responseElement.innerText = response;
        chatbotMessages.appendChild(responseElement);
      
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        }, 2000);
      });

