// document.addEventListener('DOMContentLoaded', function () {
//         var myModal = new bootstrap.Modal(document.getElementById('exampleModal'));
//         myModal.show();
// });

document.querySelectorAll(".copy-link").forEach(copyLinkContainer => {
        const inputField = copyLinkContainer.querySelector(".copy-link-input");
        const copyButton = copyLinkContainer.querySelector(".copy-link-button");

        inputField.addEventListener("focus", () => inputField.select());
        copyButton.addEventListener("click", () => {
                const text = inputField.value;

                inputField.select();
                navigator.clipboard.writeText(text);

                inputField.value = "Copied!";
                setTimeout(() => inputField.value = text, 2000)
        })
});

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

document.addEventListener("DOMContentLoaded", function () {
        const tooltipTriggerEl = document.getElementById('tooltipBtn');
        const tooltip = new bootstrap.Tooltip(tooltipTriggerEl);

        tooltip.show();

        setTimeout(() => {
                tooltip.hide();
        }, 7000);
});
