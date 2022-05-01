
// On document Ready.
$(document).ready(function(){
     $("#generate-wallet-ack").click(onGenerateAccountAck);
     $("#generate-download-wallet-ack").click(onDownloadWalletAck);
     $("#generate-copy-wallet-ack").click(onCopyWalletAck);
});

function prepareText(){
    return "wallet-id: " + $("#new-wallet-details-wallet-id").text() + "\n"
        + "secret-key: " + $("#new-wallet-details-secret-key").text() + "\n";
}

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

function onGenerateAccountAck(e) {
    $.ajax({
      url: "/api/generate-wallet-ack",
      context: document.body
    }).done(function(data) {
        $("#new-wallet-instructions").hide();
        $("#new-wallet-details,#generate-download-wallet-ack,#generate-copy-wallet-ack").show();
        $("#new-wallet-details-wallet-id").text(data["wallet-id"]);
        $("#new-wallet-details-secret-key").text(data["secret-key"]);
    });
}

function onDownloadWalletAck(e) {
    download("wallet.txt", prepareText())
}

function onCopyWalletAck(e) {
    navigator.clipboard.writeText(prepareText());
    alert("Credentials are copied to your clip-board.")
}