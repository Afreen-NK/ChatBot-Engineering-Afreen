/**
 * script.js - Client-Side Controller for CareerCompass FAQ Chatbot
 * Handles real-time messaging, category browsing, suggestion chips,
 * session storage persistence, and dynamic UI animations.
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const chatArea = document.getElementById("chatArea");
  const chatForm = document.getElementById("chatForm");
  const userInput = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");
  const typingIndicator = document.getElementById("typingIndicator");
  const clearChatBtn = document.getElementById("clearChatBtn");
  const pillsScroll = document.getElementById("pillsScroll");
  const categoryDrawer = document.getElementById("drawerDrawer") || document.getElementById("categoryDrawer");
  const drawerTitle = document.getElementById("drawerTitle");
  const drawerQuestions = document.getElementById("drawerQuestions");
  const drawerCloseBtn = document.getElementById("drawerCloseBtn");
  const openSidebarBtn = document.getElementById("openSidebarBtn");
  const closeSidebarBtn = document.getElementById("closeSidebarBtn");
  const categorySidebar = document.getElementById("categorySidebar");
  const categoryList = document.getElementById("categoryList");

  // Format current local time (e.g. "9:42 PM")
  function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  // Auto-scroll chat area to latest message
  function scrollToBottom() {
    chatArea.scrollTop = chatArea.scrollHeight;
  }

  // Auto-resize textarea as user types
  function autoResizeInput() {
    userInput.style.height = "auto";
    userInput.style.height = Math.min(userInput.scrollHeight, 120) + "px";
  }

  // Create SVG Avatar Element for Bot
  function createBotAvatar() {
    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"></circle>
        <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76" fill="currentColor"></polygon>
      </svg>
    `;
    return avatar;
  }

  // Append a message to the chat window
  function appendMessage({ sender, text, category, confidence, matchedQuestion, time }) {
    const messageRow = document.createElement("div");
    messageRow.className = `message-row ${sender === "user" ? "user-row" : "bot-row"}`;

    // Avatar
    if (sender === "user") {
      const userAvatar = document.createElement("div");
      userAvatar.className = "message-avatar";
      userAvatar.textContent = "YOU";
      messageRow.appendChild(userAvatar);
    } else {
      messageRow.appendChild(createBotAvatar());
    }

    // Content group
    const contentGroup = document.createElement("div");
    contentGroup.className = "message-content-group";

    // Message bubble
    const bubble = document.createElement("div");
    bubble.className = `message-bubble ${sender === "user" ? "user-bubble" : "bot-bubble"}`;
    bubble.textContent = text; // Safe text insertion prevents XSS
    contentGroup.appendChild(bubble);

    // Metadata row (category, confidence, timestamp)
    const meta = document.createElement("div");
    meta.className = "message-meta";

    if (category) {
      const catBadge = document.createElement("span");
      catBadge.className = "category-tag";
      catBadge.textContent = category;
      meta.appendChild(catBadge);
    }

    if (confidence && confidence > 0) {
      const confBadge = document.createElement("span");
      confBadge.className = "confidence-tag";
      const pct = Math.round(confidence * 100);
      confBadge.textContent = `${pct}% match`;
      confBadge.title = matchedQuestion ? `Matched with: "${matchedQuestion}"` : "";
      meta.appendChild(confBadge);
    }

    const timeSpan = document.createElement("span");
    timeSpan.className = "message-time";
    timeSpan.textContent = time || getCurrentTime();
    meta.appendChild(timeSpan);

    contentGroup.appendChild(meta);
    messageRow.appendChild(contentGroup);
    chatArea.appendChild(messageRow);

    scrollToBottom();
    saveSessionChat();
  }

  // Save current conversation in sessionStorage
  function saveSessionChat() {
    try {
      const messages = [];
      const rows = chatArea.querySelectorAll(".message-row:not(#welcomeMessage)");
      rows.forEach((row) => {
        const isUser = row.classList.contains("user-row");
        const bubble = row.querySelector(".message-bubble");
        const catBadge = row.querySelector(".category-tag");
        const confBadge = row.querySelector(".confidence-tag");
        const timeSpan = row.querySelector(".message-time");

        if (bubble) {
          messages.push({
            sender: isUser ? "user" : "bot",
            text: bubble.textContent,
            category: catBadge ? catBadge.textContent : null,
            confidence: confBadge ? parseFloat(confBadge.textContent) / 100 : null,
            time: timeSpan ? timeSpan.textContent : null,
          });
        }
      });
      sessionStorage.setItem("careercompass_history", JSON.stringify(messages));
    } catch (e) {
      console.warn("Could not save chat history to session storage:", e);
    }
  }

  // Restore chat history from sessionStorage
  function loadSessionChat() {
    try {
      const saved = sessionStorage.getItem("careercompass_history");
      if (saved) {
        const messages = JSON.parse(saved);
        messages.forEach((msg) => appendMessage(msg));
      }
    } catch (e) {
      console.warn("Could not load chat history from session storage:", e);
    }
  }

  // Clear chat conversation
  function clearChat() {
    sessionStorage.removeItem("careercompass_history");
    const welcome = document.getElementById("welcomeMessage");
    chatArea.innerHTML = "";
    if (welcome) {
      chatArea.appendChild(welcome);
    }
    userInput.value = "";
    userInput.focus();
  }

  // Send message to Flask API
  async function sendMessage(text) {
    const query = text.trim();
    if (!query) return;

    // Append user message immediately
    appendMessage({
      sender: "user",
      text: query,
      time: getCurrentTime(),
    });

    // Clear input
    userInput.value = "";
    userInput.style.height = "auto";
    sendBtn.disabled = true;

    // Show loading typing indicator
    typingIndicator.classList.remove("hidden");
    scrollToBottom();

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: query }),
      });

      const data = await response.json();

      // Hide typing indicator
      typingIndicator.classList.add("hidden");

      if (response.ok) {
        appendMessage({
          sender: "bot",
          text: data.answer,
          category: data.category,
          confidence: data.confidence,
          matchedQuestion: data.matched_question,
          time: getCurrentTime(),
        });
      } else {
        appendMessage({
          sender: "bot",
          text: data.answer || "Sorry, an error occurred while processing your question.",
          time: getCurrentTime(),
        });
      }
    } catch (err) {
      typingIndicator.classList.add("hidden");
      appendMessage({
        sender: "bot",
        text: "Could not reach the server. Please verify your connection or restart the app.",
        time: getCurrentTime(),
      });
      console.error("Fetch error:", err);
    } finally {
      sendBtn.disabled = false;
      userInput.focus();
    }
  }

  // Handle Form Submit
  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    sendMessage(userInput.value);
  });

  // Handle Enter key (without Shift) to send
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(userInput.value);
    }
  });

  userInput.addEventListener("input", autoResizeInput);

  // Suggested questions delegation (welcome message chips)
  document.addEventListener("click", (e) => {
    const chip = e.target.closest(".chip-btn");
    if (chip && chip.dataset.query) {
      sendMessage(chip.dataset.query);
    }
  });

  // Clear chat button listener
  clearChatBtn.addEventListener("click", () => {
    if (confirm("Are you sure you want to clear the conversation?")) {
      clearChat();
    }
  });

  // ==========================================================================
  // Category Quick Access Bar & Drawer
  // ==========================================================================

  pillsScroll.addEventListener("click", async (e) => {
    const pill = e.target.closest(".pill-btn");
    if (!pill) return;

    // Update active pill
    pillsScroll.querySelectorAll(".pill-btn").forEach((p) => p.classList.remove("active"));
    pill.classList.add("active");

    const category = pill.dataset.category;

    if (category === "all") {
      categoryDrawer.classList.add("hidden");
      return;
    }

    try {
      const res = await fetch(`/api/faqs?category=${encodeURIComponent(category)}`);
      const data = await res.json();

      if (data.status === "success" && data.faqs.length > 0) {
        drawerTitle.textContent = `${category} (${data.faqs.length} FAQs)`;
        drawerQuestions.innerHTML = "";

        data.faqs.forEach((faq) => {
          const btn = document.createElement("button");
          btn.className = "drawer-q-btn";
          btn.textContent = faq.question;
          btn.addEventListener("click", () => {
            sendMessage(faq.question);
            categoryDrawer.classList.add("hidden");
          });
          drawerQuestions.appendChild(btn);
        });

        categoryDrawer.classList.remove("hidden");
      }
    } catch (err) {
      console.error("Error loading category FAQs:", err);
    }
  });

  if (drawerCloseBtn) {
    drawerCloseBtn.addEventListener("click", () => {
      categoryDrawer.classList.add("hidden");
      const allPill = pillsScroll.querySelector('[data-category="all"]');
      if (allPill) {
        pillsScroll.querySelectorAll(".pill-btn").forEach((p) => p.classList.remove("active"));
        allPill.classList.add("active");
      }
    });
  }

  // ==========================================================================
  // Off-canvas Category Sidebar
  // ==========================================================================

  async function loadSidebarCategories() {
    try {
      const res = await fetch("/api/categories");
      const data = await res.json();
      if (data.status === "success") {
        categoryList.innerHTML = "";
        const catMap = data.categories;

        const categoryIcons = {
          "Career Paths": "🎯",
          "Programming": "💻",
          "AI/ML": "🤖",
          "Internships": "💼",
          "Placements": "🏢",
          "Resume": "📄",
          "Projects": "🛠️",
          "Certifications": "📜",
          "Higher Studies": "🎓",
          "ECE Careers": "⚡",
        };

        Object.keys(catMap).forEach((catName) => {
          const cat = catMap[catName];
          const icon = categoryIcons[catName] || "📌";

          const card = document.createElement("div");
          card.className = "category-item-card";
          card.innerHTML = `
            <div class="cat-card-header">
              <span class="cat-card-title">${icon} ${cat.name}</span>
              <span class="cat-card-count">${cat.count} FAQs</span>
            </div>
            <div class="cat-card-desc">Sample: "${cat.sample_questions[0] || ""}"</div>
          `;

          card.addEventListener("click", () => {
            // Find corresponding pill and trigger it
            const pill = pillsScroll.querySelector(`[data-category="${catName}"]`);
            if (pill) {
              pill.click();
              pill.scrollIntoView({ behavior: "smooth", inline: "center" });
            }
            categorySidebar.classList.remove("open");
          });

          categoryList.appendChild(card);
        });
      }
    } catch (err) {
      console.error("Error loading sidebar categories:", err);
    }
  }

  if (openSidebarBtn) {
    openSidebarBtn.addEventListener("click", () => {
      categorySidebar.classList.add("open");
      loadSidebarCategories();
    });
  }

  if (closeSidebarBtn) {
    closeSidebarBtn.addEventListener("click", () => {
      categorySidebar.classList.remove("open");
    });
  }

  // Close sidebar on outside click
  document.addEventListener("click", (e) => {
    if (
      categorySidebar.classList.contains("open") &&
      !categorySidebar.contains(e.target) &&
      e.target !== openSidebarBtn &&
      !openSidebarBtn.contains(e.target)
    ) {
      categorySidebar.classList.remove("open");
    }
  });

  // Restore history on load
  loadSessionChat();
});
