function onCopyEnd(success, target) {
  if (success) {
    target.getElementsByClassName("copy-text")[0].innerText = "copied !";
  } else {
    target.getElementsByClassName("copy-text")[0].innerText = "unable to copy";
  }

  setTimeout(
    (t) => {
      t.getElementsByClassName("copy-text")[0].innerText = "";
    },
    1500,
    target,
  );
}

function fallbackCopyTextToClipboard(target, text) {
  var textArea = document.createElement("textarea");
  textArea.value = text;

  // Avoid scrolling to bottom
  textArea.style.top = "0";
  textArea.style.left = "0";
  textArea.style.position = "fixed";

  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    onCopyEnd(document.execCommand("copy"), target);
  } catch (err) {
    onCopyEnd(false, target);
  }

  document.body.removeChild(textArea);
}

function copyTextToClipboard(event) {
  let target = event.target.parentElement.parentElement.parentElement;
  let text = target.getElementsByClassName("code")[0].innerText;

  if (!navigator.clipboard) {
    fallbackCopyTextToClipboard(target, text);
  } else {
    navigator.clipboard.writeText(text).then(
      function () {
        onCopyEnd(true, target);
      },
      function (err) {
        onCopyEnd(false, target);
      },
    );
  }
}

var copyBobBtn = document.querySelector(".btn-hidden");
copyBobBtn.addEventListener("click", function (event) {
  copyTextToClipboard(event);
});
