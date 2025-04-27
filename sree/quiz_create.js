function generateUniqueID(prefix = '') {
    const timestamp = Date.now().toString(36);
    const random = Math.random().toString(36).substring(2, 8);
    return prefix + timestamp + random;
  }
  
  function addQuestionBlock() {
    const container = document.getElementById("questions-container");
    const firstBlock = container.querySelector(".question-block");
    const newBlock = firstBlock.cloneNode(true);
  
    newBlock.querySelectorAll('input[type="text"]').forEach(input => input.value = "");
    newBlock.querySelectorAll('input[type="file"]').forEach(input => input.value = "");
    newBlock.querySelectorAll('select').forEach(select => select.selectedIndex = 0);
  
    const questionID = generateUniqueID("ques_");
    const createdAt = new Date().toISOString();
    newBlock.setAttribute("data-question-id", questionID);
    newBlock.setAttribute("data-created-at", createdAt);
  
    container.appendChild(newBlock);
    newBlock.scrollIntoView({ behavior: "smooth", block: "end" });
    updateLivePreview();
  }
  
  function updateLivePreview() {
    const questionBlocks = document.querySelectorAll(".question-block");
    const previewContainer = document.getElementById("questionPreview");
    previewContainer.innerHTML = "";
  
    questionBlocks.forEach((block, index) => {
      const questionTitle = block.querySelector(".question-title").value;
      const mediaInput = block.querySelector(".question-media");
      const correctAnswer = block.querySelector(".correct-answer").value;
  
      const questionPreview = document.createElement("div");
      questionPreview.classList.add("question-preview-item");
  
      const titleElem = document.createElement("p");
      titleElem.innerHTML = `<strong>Q${index + 1}:</strong> ${questionTitle}`;
      questionPreview.appendChild(titleElem);
  
      const mediaPreview = document.createElement("div");
      const file = mediaInput.files[0];
      if (file) {
        const mediaType = file.type.split("/")[0];
        if (mediaType === "image") {
          const imgElem = document.createElement("img");
          imgElem.src = URL.createObjectURL(file);
          mediaPreview.appendChild(imgElem);
        } else if (mediaType === "video") {
          const videoElem = document.createElement("video");
          videoElem.src = URL.createObjectURL(file);
          videoElem.controls = true;
          mediaPreview.appendChild(videoElem);
        }
      }
      questionPreview.appendChild(mediaPreview);
  
      const answerElem = document.createElement("p");
      answerElem.innerHTML = `<strong>Correct Answer:</strong> ${correctAnswer}`;
      questionPreview.appendChild(answerElem);
  
      previewContainer.appendChild(questionPreview);
    });
  
    syncQuizDropdown();
  }
  
  // Sync the quiz dropdown with title or existing quizzes
  function syncQuizDropdown() {
    const quizTitleInput = document.getElementById("newQuizTitle").value.trim();
    const quizDropdowns = document.querySelectorAll(".quiz-dropdown");
  
    quizDropdowns.forEach(dropdown => {
      dropdown.innerHTML = "";
  
      if (quizTitleInput !== "") {
        dropdown.innerHTML = `<option value="${quizTitleInput}" selected>${quizTitleInput} (New)</option>`;
      } else {
        const existing = [
          "Cyber Basics",
          "Gesture Mastery",
          "Advanced Sign Quiz",
          "Basics of Sign Language",
          "Daily Greetings"
        ];
        dropdown.innerHTML = `<option value="">-- Choose Quiz --</option>`;
        existing.forEach(title => {
          const opt = document.createElement("option");
          opt.value = title;
          opt.textContent = title;
          dropdown.appendChild(opt);
        });
      }
    });
  }
  
  window.onload = function () {
    const firstBlock = document.querySelector(".question-block");
    firstBlock.setAttribute("data-question-id", generateUniqueID("ques_"));
    firstBlock.setAttribute("data-created-at", new Date().toISOString());
  
    document.getElementById("btnAddQuestion").addEventListener("click", addQuestionBlock);
  
    document.getElementById("btnCreateQuiz").addEventListener("click", () => {
      const quizTitle = document.getElementById("newQuizTitle").value.trim();
      const quizDifficulty = document.getElementById("quizDifficulty").value;
      const questions = document.querySelectorAll(".question-block");
  
      if (quizTitle === "") {
        alert("Quiz title is required to create a new quiz.");
        return;
      }
      if (quizDifficulty === "") {
        alert("Please select a difficulty level.");
        return;
      }
      if (questions.length === 0) {
        alert("A quiz must contain at least one question.");
        return;
      }
  
      // ✅ Submit logic goes here (to Flask backend)
      alert(`Quiz "${quizTitle}" with ${questions.length} question(s) created!`);
    });
  
    document.getElementById("btnAddToQuiz").addEventListener("click", () => {
      const quizTitle = document.getElementById("newQuizTitle").value.trim();
      if (quizTitle !== "") {
        alert("You're entering a new quiz title — use 'Create Quiz' instead.");
        return;
      }
  
      const questions = document.querySelectorAll(".question-block");
      if (questions.length === 0) {
        alert("You must add at least one question to add to a quiz.");
        return;
      }
  
      alert("Questions added to the selected existing quiz successfully!");
    });
  
    // Live sync
    document.getElementById("newQuizTitle").addEventListener("input", syncQuizDropdown);
    syncQuizDropdown(); // run once on load
  };
  