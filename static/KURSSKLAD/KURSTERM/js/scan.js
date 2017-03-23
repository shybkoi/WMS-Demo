var _useScan_ = true;

var GScanElement=null;

//var ScannerPrefixCode = /msie 6.0/i.test(navigator.userAgent) ? 17 : 0;
var ScannerPrefixCode = 0;
var GScaning = false;
var GOnlyScanElement=null;
var GScanElementForm;

function handleScanKeyPress(evt){
      if (GScaning == 'hscan') {
          if (getKeyCode(evt) != ScannerPrefixCode) {
              GOnlyScanElement.value = GOnlyScanElement.value +  String.fromCharCode(getKeyCode(evt));
          }
          CancelAction(evt);
      }
      if (GScaning == 'no') {
          CancelAction(evt);
      }
}