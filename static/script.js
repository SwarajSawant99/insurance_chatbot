<script>
    const insuranceType = "{{ insurance_type }}";

    function handleKeyPress(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    }

    async function sendMessage() {
        const input = document.getElementById("user-input");
        const chatBox = document.getElementById("chat-box");

        const query = input.value.trim();

        if (!query) return;

        // user message
        chatBox.innerHTML += `
            <div style="text-align:right; margin:10px;">
                <b>You:</b> ${query}
            </div>
        `;

        input.value = "";

        // loading
        chatBox.innerHTML += `
            <div id="loading" style="margin:10px;">
                <b>Bot:</b> Thinking...
            </div>
        `;

        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: query,
                insurance_type: insuranceType
            })
        });

        const data = await response.json();

        document.getElementById("loading").remove();

        chatBox.innerHTML += `
            <div style="margin:10px;">
                <b>Bot:</b> ${data.answer.replace(/\n/g, "<br>")}
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;
    }
</script>