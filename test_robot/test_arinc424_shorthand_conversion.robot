*** Settings ***
Documentation    Suite description
Library   Collections
Library  ../arinc424_shorthand_conversion.py

*** Variables ***
${correct_arinc424_code}   50N60
${correct_lon}   16000W
${correct_lat}   5000N

*** Test Cases ***

Correct ARINC424 Code Is Converted To Coordinates Pair
    @{args_input}=  Create List  ${correct_arinc424_code}
    ${result}=  main  args=@{args_input}
    Should Be Equal  "${result}"  "16000W 5000N"

Correct Lon Lat Coordinates Pair Is Converted To ARINC424 Code
    @{args_input}=  Create List  ${correct_lon}  ${correct_lat}
    ${result}=  main  args=@{args_input}
    Should Be Equal  "${result}"  "50N60"