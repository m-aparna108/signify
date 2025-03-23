document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("addSignForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Stop the default form submission
    
        /*let formData = new FormData(this); // Create FormData object
    
        fetch("/add_sign", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Show success message
            fetchSigns(); // Reload the signs list
            this.reset(); // Clear the form
        })
        .catch(error => console.error("Error:", error));*/
        showConfirmationPopup(() => {
            let formData = new FormData(document.getElementById("addSignForm")); // Create FormData object

            fetch("/add_sign", {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                showToast("Sign added successfully!", "success"); // Custom popup instead of alert
                fetchSigns(); // Reload the signs list
                document.getElementById("addSignForm").reset(); // Clear the form
            })
            .catch(error => console.error("Error:", error));
        });
    
    });

    // Function to show confirmation popup
function showConfirmationPopup(callback) {
    const modal = document.createElement("div");
    modal.className = "modal-overlay";
    modal.innerHTML = `
        <div class="modal">
            <p>Are you sure you want to add this sign?</p>
            <button id="confirmAdd">Yes</button>
            <button id="cancelAdd">No</button>
        </div>
    `;
    document.body.appendChild(modal);

    document.getElementById("confirmAdd").addEventListener("click", () => {
        callback(); // Call function to submit the form
        modal.remove();
    });

    document.getElementById("cancelAdd").addEventListener("click", () => {
        modal.remove();
    });
}
    
    
    
    
    
    let currentPage = 1;

    function fetchSigns() {
        const searchQuery = document.getElementById("searchInput").value;
        const category = document.getElementById("categoryFilter").value;

        fetch(`/get_signs?page=${currentPage}&search=${searchQuery}&category=${category}`)
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById("signTableBody");
                tableBody.innerHTML = "";

                data.signs.forEach(sign => {
                    const row = document.createElement("tr");
                    row.setAttribute("data-sign-id", sign._id.$oid); // Store ID for deletion
                    row.innerHTML = `
                        <td><img src="${sign.image}" width="50"></td>
                        <td>${sign.name}</td>
                        <td>${sign.category}</td>
                        <td>${sign.description}</td>
                        <td>
                            <button onclick="editSign('${sign._id.$oid}', '${sign.name}', '${sign.description}')">Edit</button>
                            <button class="delete-btn" data-id="${sign._id.$oid}">Delete</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });

                document.getElementById("pageNumber").innerText = currentPage;
                attachDeleteListeners();
            })
            
            .catch(error => console.error("Error fetching signs:", error));
    }

    function attachDeleteListeners() {
        document.querySelectorAll(".delete-btn").forEach(button => {
            button.addEventListener("click", function () {
                const signId = this.getAttribute("data-id");
                const rowElement = this.closest("tr");
                deleteSign(signId,rowElement);
            });
        });
    }


    document.getElementById("searchInput").addEventListener("input", fetchSigns);
    document.getElementById("categoryFilter").addEventListener("change", fetchSigns);
    document.getElementById("prevPage").addEventListener("click", function () {
        if (currentPage > 1) {
            currentPage--;
            fetchSigns();
        }
    });
    document.getElementById("nextPage").addEventListener("click", function () {
        currentPage++;
        fetchSigns();
    });

    fetchSigns();



});
/*
function editSign(signId, name, description, imageUrl) {
    const modal = document.getElementById("editSignModal");
    modal.style.display = "block"; // Show modal

    // Fill form with existing data
    document.getElementById("editSignId").value = signId;
    document.getElementById("editSignName").value = name;
    document.getElementById("editSignDescription").value = description;

    // Show current image
    document.getElementById("currentSignImage").src = imageUrl;
}
// Handle form submission for edit
document.getElementById("editSignForm").addEventListener("submit", function (event) {
    event.preventDefault();

    let signId = document.getElementById("editSignId").value;
    let formData = new FormData();
    formData.append("name", document.getElementById("editSignName").value);
    formData.append("description", document.getElementById("editSignDescription").value);

    let imageInput = document.getElementById("editSignImage");
    if (imageInput.files.length > 0) {
        formData.append("image", imageInput.files[0]); // Add new image only if selected
    }
    // Debugging: Log what is being sent
    //for (let pair of formData.entries()) {
       // console.log(pair[0], pair[1]);
    //}

    fetch(`/update_sign/${signId}`, {
        method: "PUT",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server Response:", data); // Log response from the backend
        alert(data.message);
        document.getElementById("editSignModal").style.display = "none"; // Hide modal
        fetchSigns(); // Refresh list
    })
    .catch(error => console.error("Update Error:", error));
});

// Close modal when clicking the "X"
document.querySelector(".close").addEventListener("click", function () {
    document.getElementById("editSignModal").style.display = "none";
});
*/
function editSign(signId, name, description, imageUrl) {
    const modal = document.getElementById("editSignModal");
    modal.style.display = "block"; // Show modal

    // Fill form with existing data
    document.getElementById("editSignId").value = signId;
    document.getElementById("editSignName").value = name;
    document.getElementById("editSignDescription").value = description;

    // Display current image
    let currentImage = document.getElementById("currentSignImage");
    currentImage.src = imageUrl ? imageUrl : "static/sign_images/default.jpg"; // Default image if missing
}

// Handle form submission for editing a sign
document.getElementById("editSignForm").addEventListener("submit", function (event) {
    event.preventDefault();

    let signId = document.getElementById("editSignId").value;
    let formData = new FormData();
    formData.append("name", document.getElementById("editSignName").value);
    formData.append("description", document.getElementById("editSignDescription").value);

    let imageInput = document.getElementById("editSignImage");
    if (imageInput.files.length > 0) {
        formData.append("image", imageInput.files[0]); // Add new image if selected
    }

    fetch(`/update_sign/${signId}`, {
        method: "PUT",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        //alert(data.error);
        document.getElementById("editSignModal").style.display = "none"; // Hide modal
        fetchSigns(); // Refresh list
    })
    .catch(error => console.error("Update Error:", error));
});

// Close modal when clicking the "X"
document.querySelector(".close").addEventListener("click", function () {
    document.getElementById("editSignModal").style.display = "none";
});






// Attach edit function to buttons
function fetchSigns() {
    fetch("/get_signs")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("signTableBody");
            tableBody.innerHTML = "";

            data.signs.forEach(sign => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td><img src="${sign.image}" width="50"></td>
                    <td>${sign.name}</td>
                    <td>${sign.category}</td>
                    <td>${sign.description}</td>
                    <td>
                        <button onclick="editSign('${sign._id.$oid}', '${sign.name}', '${sign.description}', '${sign.image}')">Edit</button>
                        <button onclick="deleteSign('${sign._id.$oid}')">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        });
}


/*edidting
function editSign(signId, currentName, currentDescription) {
    document.getElementById("editSignId").value = signId;
    document.getElementById("editName").value = currentName;
    document.getElementById("editDescription").value = currentDescription;

    document.getElementById("editSignModal").style.display = "block";
}

// Handle form submission for editing
document.getElementById("editSignForm").addEventListener("submit", function (event) {
    event.preventDefault();
    
    const signId = document.getElementById("editSignId").value;
    const updatedName = document.getElementById("editName").value;
    const updatedDescription = document.getElementById("editDescription").value;

    fetch(`/edit_sign/${signId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: updatedName,
            description: updatedDescription
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById("editSignModal").style.display = "none";
        fetchSigns();  // Refresh the table after editing
    })
    .catch(error => console.error("Error:", error));
});*/


/*deleting*/



/*
let selectedSignId = null; // Global variable to store signId

function openDeleteModal(signId) {
    selectedSignId = signId; // Store the sign ID
    console.log("Selected signId:", selectedSignId); // Debugging
    document.getElementById("deleteSignModal").style.display = "block";
}

document.getElementById("confirmDelete").addEventListener("click", function() {
    if (!selectedSignId) {
        console.error("No signId selected for deletion.");
        return;
    }

    fetch(`/delete_sign/${selectedSignId}`, {
        method: "DELETE",
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(`Server Error: ${text}`);
            });
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        document.getElementById("deleteSignModal").style.display = "none"; // Hide modal
        fetchSigns();  // Refresh the sign list
    })
    .catch(error => console.error("Deletion Error:", error.message));
});

document.getElementById("cancelDelete").addEventListener("click", function() {
    document.getElementById("deleteSignModal").style.display = "none"; // Hide modal
});
*/
/*this code works-------------------------
function deleteSign(signId) {
    console.log("Deleting Sign ID:", signId); // Debugging

    // Ensure signId is a string and 24 characters long
    if (typeof signId !== "string" || signId.length !== 24) {
        console.error("Invalid signId format:", signId);
        alert("Invalid sign ID format. Deletion aborted.");
        return;
    }
    if (confirm("Are you sure you want to delete this sign?")) {
        fetch(`/delete_sign/${signId}`, {
            method: "DELETE",
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`Server Error: ${text}`);
                });
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            fetchSigns();  // Refresh sign list
        })
        .catch(error => console.error("Deletion Error:", error.message));
    }
}

*/
function deleteSign(signId, rowElement) {
    console.log("Deleting Sign ID:", signId);

    if (typeof signId !== "string" || signId.length !== 24) {
        showToast("Invalid sign ID format. Deletion aborted.", "error");
        return;
    }

    fetch(`/delete_sign/${signId}`, {
        method: "DELETE",
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showToast(data.error, "error");
        } else {
            showToast("Sign deleted successfully!", "success");
            rowElement.remove(); // Remove row instantly
        }
    })
    .catch(error => {
        console.error("Deletion Error:", error);
        showToast("Failed to delete sign. Try again.", "error");
    });
}

function showToast(message, type) {
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.innerText = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}



