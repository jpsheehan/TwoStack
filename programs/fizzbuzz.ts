{[`]$[.;];$}|print
{$0$[:10%48+`10//]$[`];$}|asciidec
30|max

$1 1
[
  ;$

  {
    {
      {
        # else print number
        $:`$ # get a copy of counter
        asciidec@
        $0$print@10.
        
      }
      {;
        # if divisible by 5 then print buzz
        0$0$"Buzz"10print@
      {}0}

      $:`$ # get a copy of the counter
      5%0=?;@ # check for divisibility
    }
    {;
      # if divisible by 3 then print fizz
      0$0$"Fizz"10print@
    {}0}
    
    $:`$ # get a copy of the counter
    3%0=?;@ # check for divisibility
  }
  {;
    # if divisible by 5 and 3
    0$0$"Fizzbuzz"10print@
  {}0}

  $:`$: # push the 2 copies of the counter onto the main stack
  
  3%0=\5%0=&
  ?;@
  
  # increment the counter and break the loop if it is less than or equal to 0
  $1+:max<
]