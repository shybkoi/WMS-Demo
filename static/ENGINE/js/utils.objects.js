function listProperties(obj, objName) {
  var result = "";
  for (var i in obj) {
    try {
      result += objName + "." + i + "=" + obj[i] + "\n";}
    catch(e)
    {}
  }
  return result;
}

function objectIsEmpty(obj)
{
  for (var i in obj) return false;
  return true;
}

function objectToString(obj) {
  var val, output = "";
  if (obj) {
    output += "{ "; //space need
    
    for (var i in obj) {
      val = obj[i];

      switch (typeof val){
        case ("object"):
          if (val==null)
            output += i + ":null,";
          else if (val[0]) {
            output += i + ":" + arrayToString(val) + ",";
          } else {
            output += i + ":" + objectToString(val) + ",";
          }
          break;
        case("string"):
          output += i + ":'"+ escape(val) + "',";
          break;
        default:
          output += i + ":" + val + ",";
      }
    }
    output = output.substring(0, output.length-1) + "}";
  }
  return output;
}

function arrayToString(array){
    var output = "";
    if (array){
        output += "[ "; //space need
        for (var i in array) {
            val = array[i];
            switch (typeof val) {
                case ("object"):
                    if (val==null)
                      output += i + ":null,";
                    else if (val[0])
                      output += arrayToString(val) + ",";
                    else
                      output += objectToString(val) + ",";
                    break;
                case ("string"):
                    output += "'" + escape(val) + "',";
                    break;
                default:
                    output += val + ",";
            }
        }
        output = output.substring(0, output.length-1) + "]";
    }
    return output;
}

function stringTo0bject(string){
  eval("var result = " + string);
  return result;
}

function stringToArray(string){
  eval("var result = " + string);
  return result;
}
