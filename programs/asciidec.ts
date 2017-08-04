{
  $0$ # push a zero to the other stack (we will use it to store our string)
  [
    : # copy the number
    10%48+ # get the ascii character of the least significant digit and push it to the ztack
    `
    10//
  ]$
}|asciidec

0$0$
12345678asciidec@

[.;]$ _