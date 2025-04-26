document.addEventListener("DOMContentLoaded", function () {
    const profileIcon = document.getElementById("profileIcon");
    const profileCard = document.getElementById("profileCard");
    const logoutBtn = document.getElementById("logoutBtn");
    const logoutModal = document.getElementById("logoutModal");
    const cancelLogout = document.getElementById("cancelLogout");

    // Toggle Profile Dropdown
    profileIcon.addEventListener("click", function () {
        profileCard.style.display = (profileCard.style.display === "block") ? "none" : "block";
    });

    // Show Logout Confirmation Modal
    logoutBtn.addEventListener("click", function () {
        logoutModal.style.display = "flex";
    });

    // Hide Logout Modal
    cancelLogout.addEventListener("click", function () {
        logoutModal.style.display = "none";
    });
});
document.getElementById("confirmLogout").addEventListener("click", function () {
    window.location.href = "/logout";
});



/*search learning module------------------------*/
function filterCards() {
    let input = document.getElementById("searchinput").value.toLowerCase();
    let cards = document.querySelectorAll(".sign-card");

    cards.forEach(card => {
        let name = card.querySelector("h3").innerText.toLowerCase();
        let description = card.querySelector("p").innerText.toLowerCase();

        if (name.includes(input) || description.includes(input)) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}
