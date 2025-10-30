$(document).ready(function () {
  $("#contactForm").on("submit", function (e) {
    e.preventDefault(); // Prevent default form submission

    const formMethod = $(this).attr("method");
    const formAction = $(this).attr("action");

    $(".invalid-feedback").remove();
    $(".is-invalid").removeClass("is-invalid");

    $.ajax({
      url: formAction,
      type: formMethod,
      data: $("#contactForm").serialize(),
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
      success: function (response) {
        $("#successSubmissionModalMessage").text(response.message);
        $("#successSubmissionModal").modal("show");
        $("#contactForm")[0].reset();
      },
      error: function (response) {
        const resp = response.responseJSON;
        for (const [fieldName, errorMessages] of Object.entries(resp.errors)) {
          const fieldElement = $(`#id_${fieldName}`);
          if (fieldElement.length) {
            fieldElement.addClass("is-invalid");
            const errorDiv = $('<div class="invalid-feedback d-block"></div>');
            errorDiv.text(errorMessages.join(", "));
            fieldElement.after(errorDiv);
          }
        }
      },
    });
  });
});
