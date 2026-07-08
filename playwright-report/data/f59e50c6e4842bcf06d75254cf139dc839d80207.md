# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: orangehrm-comprehensive-sub-functions.spec.ts >> ADMIN: User Management >> WF-1.1: View all system users list
- Location: tests/e2e/orangehrm-comprehensive-sub-functions.spec.ts:30:7

# Error details

```
Error: expect(received).toBeGreaterThan(expected)

Expected: > 0
Received:   0
```

# Page snapshot

```yaml
- generic [ref=e3]:
  - generic:
    - complementary [ref=e4]:
      - navigation "Sidepanel" [ref=e5]:
        - generic [ref=e6]:
          - link "client brand banner" [ref=e7] [cursor=pointer]:
            - /url: https://www.orangehrm.com/
            - img "client brand banner" [ref=e9]
          - text: 
        - generic [ref=e10]:
          - generic [ref=e11]:
            - generic [ref=e12]:
              - textbox "Search" [ref=e15]
              - button "" [ref=e16] [cursor=pointer]:
                - generic [ref=e17]: 
            - separator [ref=e18]
          - list [ref=e19]:
            - listitem [ref=e20]:
              - link "Admin" [ref=e21] [cursor=pointer]:
                - /url: /web/index.php/admin/viewAdminModule
                - generic [ref=e24]: Admin
            - listitem [ref=e25]:
              - link "PIM" [ref=e26] [cursor=pointer]:
                - /url: /web/index.php/pim/viewPimModule
                - generic [ref=e40]: PIM
            - listitem [ref=e41]:
              - link "Leave" [ref=e42] [cursor=pointer]:
                - /url: /web/index.php/leave/viewLeaveModule
                - generic [ref=e45]: Leave
            - listitem [ref=e46]:
              - link "Time" [ref=e47] [cursor=pointer]:
                - /url: /web/index.php/time/viewTimeModule
                - generic [ref=e53]: Time
            - listitem [ref=e54]:
              - link "Recruitment" [ref=e55] [cursor=pointer]:
                - /url: /web/index.php/recruitment/viewRecruitmentModule
                - generic [ref=e61]: Recruitment
            - listitem [ref=e62]:
              - link "My Info" [ref=e63] [cursor=pointer]:
                - /url: /web/index.php/pim/viewMyDetails
                - generic [ref=e69]: My Info
            - listitem [ref=e70]:
              - link "Performance" [ref=e71] [cursor=pointer]:
                - /url: /web/index.php/performance/viewPerformanceModule
                - generic [ref=e79]: Performance
            - listitem [ref=e80]:
              - link "Dashboard" [ref=e81] [cursor=pointer]:
                - /url: /web/index.php/dashboard/index
                - generic [ref=e84]: Dashboard
            - listitem [ref=e85]:
              - link "Directory" [ref=e86] [cursor=pointer]:
                - /url: /web/index.php/directory/viewDirectory
                - generic [ref=e89]: Directory
            - listitem [ref=e90]:
              - link "Maintenance" [ref=e91] [cursor=pointer]:
                - /url: /web/index.php/maintenance/viewMaintenanceModule
                - generic [ref=e95]: Maintenance
            - listitem [ref=e96]:
              - link "Claim" [ref=e97] [cursor=pointer]:
                - /url: /web/index.php/claim/viewClaimModule
                - img [ref=e100]
                - generic [ref=e104]: Claim
            - listitem [ref=e105]:
              - link "Buzz" [ref=e106] [cursor=pointer]:
                - /url: /web/index.php/buzz/viewBuzz
                - generic [ref=e109]: Buzz
    - banner [ref=e110]:
      - generic [ref=e111]:
        - generic [ref=e112]:
          - text: 
          - generic [ref=e113]:
            - heading "Admin" [level=6] [ref=e114]
            - heading "/ User Management" [level=6] [ref=e115]
        - link "Upgrade" [ref=e117]:
          - /url: https://orangehrm.com/open-source/upgrade-to-advanced
          - button "Upgrade" [ref=e118] [cursor=pointer]: Upgrade
        - list [ref=e124]:
          - listitem [ref=e125]:
            - generic [ref=e126] [cursor=pointer]:
              - img "profile picture" [ref=e127]
              - paragraph [ref=e128]: Test NewLastName
              - generic [ref=e129]: 
      - navigation "Topbar Menu" [ref=e131]:
        - list [ref=e132]:
          - listitem [ref=e133] [cursor=pointer]:
            - generic [ref=e134]:
              - text: User Management
              - generic [ref=e135]: 
          - listitem [ref=e136] [cursor=pointer]:
            - generic [ref=e137]:
              - text: Job
              - generic [ref=e138]: 
          - listitem [ref=e139] [cursor=pointer]:
            - generic [ref=e140]:
              - text: Organization
              - generic [ref=e141]: 
          - listitem [ref=e142] [cursor=pointer]:
            - generic [ref=e143]:
              - text: Qualifications
              - generic [ref=e144]: 
          - listitem [ref=e145] [cursor=pointer]:
            - link "Nationalities" [ref=e146]:
              - /url: "#"
          - listitem [ref=e147] [cursor=pointer]:
            - link "Corporate Branding" [ref=e148]:
              - /url: "#"
          - listitem [ref=e149] [cursor=pointer]:
            - generic [ref=e150]:
              - text: Configuration
              - generic [ref=e151]: 
          - button "" [ref=e153] [cursor=pointer]:
            - generic [ref=e154]: 
  - generic [ref=e155]:
    - generic [ref=e157]:
      - generic [ref=e158]:
        - generic [ref=e159]:
          - heading "System Users" [level=5] [ref=e161]
          - button "" [ref=e164] [cursor=pointer]:
            - generic [ref=e165]: 
        - separator [ref=e166]
        - generic [ref=e168]:
          - generic [ref=e170]:
            - generic [ref=e172]:
              - generic [ref=e174]: Username
              - textbox [ref=e176]
            - generic [ref=e178]:
              - generic [ref=e180]: User Role
              - generic [ref=e183] [cursor=pointer]:
                - generic [ref=e184]: "-- Select --"
                - generic [ref=e186]: 
            - generic [ref=e188]:
              - generic [ref=e190]: Employee Name
              - textbox "Type for hints..." [ref=e194]
            - generic [ref=e196]:
              - generic [ref=e198]: Status
              - generic [ref=e201] [cursor=pointer]:
                - generic [ref=e202]: "-- Select --"
                - generic [ref=e204]: 
          - separator [ref=e205]
          - generic [ref=e206]:
            - button "Reset" [ref=e207] [cursor=pointer]
            - button "Search" [ref=e208] [cursor=pointer]
      - generic [ref=e209]:
        - button " Add" [ref=e211] [cursor=pointer]:
          - generic [ref=e212]: 
          - text: Add
        - generic [ref=e213]:
          - separator [ref=e214]
          - generic [ref=e216]: (26) Records Found
        - table [ref=e218]:
          - rowgroup [ref=e219]:
            - row " Username  User Role  Employee Name  Status  Actions" [ref=e220]:
              - columnheader "" [ref=e221]:
                - generic [ref=e223] [cursor=pointer]:
                  - checkbox "" [ref=e224]
                  - generic [ref=e226]: 
              - columnheader "Username " [ref=e227]:
                - text: Username
                - generic [ref=e228]:
                  - generic [ref=e229] [cursor=pointer]: 
                  - text:  
              - columnheader "User Role " [ref=e230]:
                - text: User Role
                - generic [ref=e231]:
                  - generic [ref=e232] [cursor=pointer]: 
                  - text:  
              - columnheader "Employee Name " [ref=e233]:
                - text: Employee Name
                - generic [ref=e234]:
                  - generic [ref=e235] [cursor=pointer]: 
                  - text:  
              - columnheader "Status " [ref=e236]:
                - text: Status
                - generic [ref=e237]:
                  - generic [ref=e238] [cursor=pointer]: 
                  - text:  
              - columnheader "Actions" [ref=e239]
          - rowgroup [ref=e240]:
            - row " Admin Admin Test NewLastName Enabled  " [ref=e242]:
              - cell "" [ref=e243]:
                - generic [ref=e247]:
                  - checkbox "" [ref=e248]
                  - generic [ref=e250]: 
              - cell "Admin" [ref=e251]:
                - generic [ref=e252]: Admin
              - cell "Admin" [ref=e253]:
                - generic [ref=e254]: Admin
              - cell "Test NewLastName" [ref=e255]:
                - generic [ref=e256]: Test NewLastName
              - cell "Enabled" [ref=e257]:
                - generic [ref=e258]: Enabled
              - cell " " [ref=e259]:
                - generic [ref=e260]:
                  - button "" [ref=e261] [cursor=pointer]:
                    - generic [ref=e262]: 
                  - button "" [ref=e263] [cursor=pointer]:
                    - generic [ref=e264]: 
            - row " hrmsqa1783404889 ESS Test NewLastName Enabled  " [ref=e266]:
              - cell "" [ref=e267]:
                - generic [ref=e270] [cursor=pointer]:
                  - checkbox "" [ref=e271]
                  - generic [ref=e273]: 
              - cell "hrmsqa1783404889" [ref=e274]:
                - generic [ref=e275]: hrmsqa1783404889
              - cell "ESS" [ref=e276]:
                - generic [ref=e277]: ESS
              - cell "Test NewLastName" [ref=e278]:
                - generic [ref=e279]: Test NewLastName
              - cell "Enabled" [ref=e280]:
                - generic [ref=e281]: Enabled
              - cell " " [ref=e282]:
                - generic [ref=e283]:
                  - button "" [ref=e284] [cursor=pointer]:
                    - generic [ref=e285]: 
                  - button "" [ref=e286] [cursor=pointer]:
                    - generic [ref=e287]: 
            - row " Jacey.Cole-Rodriguez@mail.com ESS Jacey Cole-Rodriguez Enabled  " [ref=e289]:
              - cell "" [ref=e290]:
                - generic [ref=e293] [cursor=pointer]:
                  - checkbox "" [ref=e294]
                  - generic [ref=e296]: 
              - cell "Jacey.Cole-Rodriguez@mail.com" [ref=e297]:
                - generic [ref=e298]: Jacey.Cole-Rodriguez@mail.com
              - cell "ESS" [ref=e299]:
                - generic [ref=e300]: ESS
              - cell "Jacey Cole-Rodriguez" [ref=e301]:
                - generic [ref=e302]: Jacey Cole-Rodriguez
              - cell "Enabled" [ref=e303]:
                - generic [ref=e304]: Enabled
              - cell " " [ref=e305]:
                - generic [ref=e306]:
                  - button "" [ref=e307] [cursor=pointer]:
                    - generic [ref=e308]: 
                  - button "" [ref=e309] [cursor=pointer]:
                    - generic [ref=e310]: 
            - row " Jobinsam@6742 ESS Jobin Sam Enabled  " [ref=e312]:
              - cell "" [ref=e313]:
                - generic [ref=e316] [cursor=pointer]:
                  - checkbox "" [ref=e317]
                  - generic [ref=e319]: 
              - cell "Jobinsam@6742" [ref=e320]:
                - generic [ref=e321]: Jobinsam@6742
              - cell "ESS" [ref=e322]:
                - generic [ref=e323]: ESS
              - cell "Jobin Sam" [ref=e324]:
                - generic [ref=e325]: Jobin Sam
              - cell "Enabled" [ref=e326]:
                - generic [ref=e327]: Enabled
              - cell " " [ref=e328]:
                - generic [ref=e329]:
                  - button "" [ref=e330] [cursor=pointer]:
                    - generic [ref=e331]: 
                  - button "" [ref=e332] [cursor=pointer]:
                    - generic [ref=e333]: 
            - row " johndoe.qa228916 ESS John Doe Enabled  " [ref=e335]:
              - cell "" [ref=e336]:
                - generic [ref=e339] [cursor=pointer]:
                  - checkbox "" [ref=e340]
                  - generic [ref=e342]: 
              - cell "johndoe.qa228916" [ref=e343]:
                - generic [ref=e344]: johndoe.qa228916
              - cell "ESS" [ref=e345]:
                - generic [ref=e346]: ESS
              - cell "John Doe" [ref=e347]:
                - generic [ref=e348]: John Doe
              - cell "Enabled" [ref=e349]:
                - generic [ref=e350]: Enabled
              - cell " " [ref=e351]:
                - generic [ref=e352]:
                  - button "" [ref=e353] [cursor=pointer]:
                    - generic [ref=e354]: 
                  - button "" [ref=e355] [cursor=pointer]:
                    - generic [ref=e356]: 
            - row " johndoe.qa497303 ESS John Doe Enabled  " [ref=e358]:
              - cell "" [ref=e359]:
                - generic [ref=e362] [cursor=pointer]:
                  - checkbox "" [ref=e363]
                  - generic [ref=e365]: 
              - cell "johndoe.qa497303" [ref=e366]:
                - generic [ref=e367]: johndoe.qa497303
              - cell "ESS" [ref=e368]:
                - generic [ref=e369]: ESS
              - cell "John Doe" [ref=e370]:
                - generic [ref=e371]: John Doe
              - cell "Enabled" [ref=e372]:
                - generic [ref=e373]: Enabled
              - cell " " [ref=e374]:
                - generic [ref=e375]:
                  - button "" [ref=e376] [cursor=pointer]:
                    - generic [ref=e377]: 
                  - button "" [ref=e378] [cursor=pointer]:
                    - generic [ref=e379]: 
            - row " johndoe.qa502205 ESS John Doe Enabled  " [ref=e381]:
              - cell "" [ref=e382]:
                - generic [ref=e385] [cursor=pointer]:
                  - checkbox "" [ref=e386]
                  - generic [ref=e388]: 
              - cell "johndoe.qa502205" [ref=e389]:
                - generic [ref=e390]: johndoe.qa502205
              - cell "ESS" [ref=e391]:
                - generic [ref=e392]: ESS
              - cell "John Doe" [ref=e393]:
                - generic [ref=e394]: John Doe
              - cell "Enabled" [ref=e395]:
                - generic [ref=e396]: Enabled
              - cell " " [ref=e397]:
                - generic [ref=e398]:
                  - button "" [ref=e399] [cursor=pointer]:
                    - generic [ref=e400]: 
                  - button "" [ref=e401] [cursor=pointer]:
                    - generic [ref=e402]: 
            - row " johndoe.qa513873 ESS John Doe Enabled  " [ref=e404]:
              - cell "" [ref=e405]:
                - generic [ref=e408] [cursor=pointer]:
                  - checkbox "" [ref=e409]
                  - generic [ref=e411]: 
              - cell "johndoe.qa513873" [ref=e412]:
                - generic [ref=e413]: johndoe.qa513873
              - cell "ESS" [ref=e414]:
                - generic [ref=e415]: ESS
              - cell "John Doe" [ref=e416]:
                - generic [ref=e417]: John Doe
              - cell "Enabled" [ref=e418]:
                - generic [ref=e419]: Enabled
              - cell " " [ref=e420]:
                - generic [ref=e421]:
                  - button "" [ref=e422] [cursor=pointer]:
                    - generic [ref=e423]: 
                  - button "" [ref=e424] [cursor=pointer]:
                    - generic [ref=e425]: 
            - row " johndoe.qa602794 ESS John Doe Enabled  " [ref=e427]:
              - cell "" [ref=e428]:
                - generic [ref=e431] [cursor=pointer]:
                  - checkbox "" [ref=e432]
                  - generic [ref=e434]: 
              - cell "johndoe.qa602794" [ref=e435]:
                - generic [ref=e436]: johndoe.qa602794
              - cell "ESS" [ref=e437]:
                - generic [ref=e438]: ESS
              - cell "John Doe" [ref=e439]:
                - generic [ref=e440]: John Doe
              - cell "Enabled" [ref=e441]:
                - generic [ref=e442]: Enabled
              - cell " " [ref=e443]:
                - generic [ref=e444]:
                  - button "" [ref=e445] [cursor=pointer]:
                    - generic [ref=e446]: 
                  - button "" [ref=e447] [cursor=pointer]:
                    - generic [ref=e448]: 
            - row " johndoe.qa679529 ESS John Doe Enabled  " [ref=e450]:
              - cell "" [ref=e451]:
                - generic [ref=e454] [cursor=pointer]:
                  - checkbox "" [ref=e455]
                  - generic [ref=e457]: 
              - cell "johndoe.qa679529" [ref=e458]:
                - generic [ref=e459]: johndoe.qa679529
              - cell "ESS" [ref=e460]:
                - generic [ref=e461]: ESS
              - cell "John Doe" [ref=e462]:
                - generic [ref=e463]: John Doe
              - cell "Enabled" [ref=e464]:
                - generic [ref=e465]: Enabled
              - cell " " [ref=e466]:
                - generic [ref=e467]:
                  - button "" [ref=e468] [cursor=pointer]:
                    - generic [ref=e469]: 
                  - button "" [ref=e470] [cursor=pointer]:
                    - generic [ref=e471]: 
            - row " johndoe.qa741897 ESS John Doe Enabled  " [ref=e473]:
              - cell "" [ref=e474]:
                - generic [ref=e477] [cursor=pointer]:
                  - checkbox "" [ref=e478]
                  - generic [ref=e480]: 
              - cell "johndoe.qa741897" [ref=e481]:
                - generic [ref=e482]: johndoe.qa741897
              - cell "ESS" [ref=e483]:
                - generic [ref=e484]: ESS
              - cell "John Doe" [ref=e485]:
                - generic [ref=e486]: John Doe
              - cell "Enabled" [ref=e487]:
                - generic [ref=e488]: Enabled
              - cell " " [ref=e489]:
                - generic [ref=e490]:
                  - button "" [ref=e491] [cursor=pointer]:
                    - generic [ref=e492]: 
                  - button "" [ref=e493] [cursor=pointer]:
                    - generic [ref=e494]: 
            - row " johndoe.qa778500 ESS John Doe Enabled  " [ref=e496]:
              - cell "" [ref=e497]:
                - generic [ref=e500] [cursor=pointer]:
                  - checkbox "" [ref=e501]
                  - generic [ref=e503]: 
              - cell "johndoe.qa778500" [ref=e504]:
                - generic [ref=e505]: johndoe.qa778500
              - cell "ESS" [ref=e506]:
                - generic [ref=e507]: ESS
              - cell "John Doe" [ref=e508]:
                - generic [ref=e509]: John Doe
              - cell "Enabled" [ref=e510]:
                - generic [ref=e511]: Enabled
              - cell " " [ref=e512]:
                - generic [ref=e513]:
                  - button "" [ref=e514] [cursor=pointer]:
                    - generic [ref=e515]: 
                  - button "" [ref=e516] [cursor=pointer]:
                    - generic [ref=e517]: 
            - row " johndoe.qa800947 ESS John Doe Enabled  " [ref=e519]:
              - cell "" [ref=e520]:
                - generic [ref=e523] [cursor=pointer]:
                  - checkbox "" [ref=e524]
                  - generic [ref=e526]: 
              - cell "johndoe.qa800947" [ref=e527]:
                - generic [ref=e528]: johndoe.qa800947
              - cell "ESS" [ref=e529]:
                - generic [ref=e530]: ESS
              - cell "John Doe" [ref=e531]:
                - generic [ref=e532]: John Doe
              - cell "Enabled" [ref=e533]:
                - generic [ref=e534]: Enabled
              - cell " " [ref=e535]:
                - generic [ref=e536]:
                  - button "" [ref=e537] [cursor=pointer]:
                    - generic [ref=e538]: 
                  - button "" [ref=e539] [cursor=pointer]:
                    - generic [ref=e540]: 
            - row " Lewis.Harvey@mail.com ESS Lewis Harvey Enabled  " [ref=e542]:
              - cell "" [ref=e543]:
                - generic [ref=e546] [cursor=pointer]:
                  - checkbox "" [ref=e547]
                  - generic [ref=e549]: 
              - cell "Lewis.Harvey@mail.com" [ref=e550]:
                - generic [ref=e551]: Lewis.Harvey@mail.com
              - cell "ESS" [ref=e552]:
                - generic [ref=e553]: ESS
              - cell "Lewis Harvey" [ref=e554]:
                - generic [ref=e555]: Lewis Harvey
              - cell "Enabled" [ref=e556]:
                - generic [ref=e557]: Enabled
              - cell " " [ref=e558]:
                - generic [ref=e559]:
                  - button "" [ref=e560] [cursor=pointer]:
                    - generic [ref=e561]: 
                  - button "" [ref=e562] [cursor=pointer]:
                    - generic [ref=e563]: 
            - row " mamidi_prasad Admin Mamidi Varma Enabled  " [ref=e565]:
              - cell "" [ref=e566]:
                - generic [ref=e569] [cursor=pointer]:
                  - checkbox "" [ref=e570]
                  - generic [ref=e572]: 
              - cell "mamidi_prasad" [ref=e573]:
                - generic [ref=e574]: mamidi_prasad
              - cell "Admin" [ref=e575]:
                - generic [ref=e576]: Admin
              - cell "Mamidi Varma" [ref=e577]:
                - generic [ref=e578]: Mamidi Varma
              - cell "Enabled" [ref=e579]:
                - generic [ref=e580]: Enabled
              - cell " " [ref=e581]:
                - generic [ref=e582]:
                  - button "" [ref=e583] [cursor=pointer]:
                    - generic [ref=e584]: 
                  - button "" [ref=e585] [cursor=pointer]:
                    - generic [ref=e586]: 
            - row " MansiUser1783407426020 ESS Mansi Thakare Enabled  " [ref=e588]:
              - cell "" [ref=e589]:
                - generic [ref=e592] [cursor=pointer]:
                  - checkbox "" [ref=e593]
                  - generic [ref=e595]: 
              - cell "MansiUser1783407426020" [ref=e596]:
                - generic [ref=e597]: MansiUser1783407426020
              - cell "ESS" [ref=e598]:
                - generic [ref=e599]: ESS
              - cell "Mansi Thakare" [ref=e600]:
                - generic [ref=e601]: Mansi Thakare
              - cell "Enabled" [ref=e602]:
                - generic [ref=e603]: Enabled
              - cell " " [ref=e604]:
                - generic [ref=e605]:
                  - button "" [ref=e606] [cursor=pointer]:
                    - generic [ref=e607]: 
                  - button "" [ref=e608] [cursor=pointer]:
                    - generic [ref=e609]: 
            - row " MansiUser1783407765982 ESS Mansi Thakare Enabled  " [ref=e611]:
              - cell "" [ref=e612]:
                - generic [ref=e615] [cursor=pointer]:
                  - checkbox "" [ref=e616]
                  - generic [ref=e618]: 
              - cell "MansiUser1783407765982" [ref=e619]:
                - generic [ref=e620]: MansiUser1783407765982
              - cell "ESS" [ref=e621]:
                - generic [ref=e622]: ESS
              - cell "Mansi Thakare" [ref=e623]:
                - generic [ref=e624]: Mansi Thakare
              - cell "Enabled" [ref=e625]:
                - generic [ref=e626]: Enabled
              - cell " " [ref=e627]:
                - generic [ref=e628]:
                  - button "" [ref=e629] [cursor=pointer]:
                    - generic [ref=e630]: 
                  - button "" [ref=e631] [cursor=pointer]:
                    - generic [ref=e632]: 
            - row " pimuser07883456 ESS Raj ravi Enabled  " [ref=e634]:
              - cell "" [ref=e635]:
                - generic [ref=e638] [cursor=pointer]:
                  - checkbox "" [ref=e639]
                  - generic [ref=e641]: 
              - cell "pimuser07883456" [ref=e642]:
                - generic [ref=e643]: pimuser07883456
              - cell "ESS" [ref=e644]:
                - generic [ref=e645]: ESS
              - cell "Raj ravi" [ref=e646]:
                - generic [ref=e647]: Raj ravi
              - cell "Enabled" [ref=e648]:
                - generic [ref=e649]: Enabled
              - cell " " [ref=e650]:
                - generic [ref=e651]:
                  - button "" [ref=e652] [cursor=pointer]:
                    - generic [ref=e653]: 
                  - button "" [ref=e654] [cursor=pointer]:
                    - generic [ref=e655]: 
            - row " pimuser08089675 ESS Raj ravi Enabled  " [ref=e657]:
              - cell "" [ref=e658]:
                - generic [ref=e661] [cursor=pointer]:
                  - checkbox "" [ref=e662]
                  - generic [ref=e664]: 
              - cell "pimuser08089675" [ref=e665]:
                - generic [ref=e666]: pimuser08089675
              - cell "ESS" [ref=e667]:
                - generic [ref=e668]: ESS
              - cell "Raj ravi" [ref=e669]:
                - generic [ref=e670]: Raj ravi
              - cell "Enabled" [ref=e671]:
                - generic [ref=e672]: Enabled
              - cell " " [ref=e673]:
                - generic [ref=e674]:
                  - button "" [ref=e675] [cursor=pointer]:
                    - generic [ref=e676]: 
                  - button "" [ref=e677] [cursor=pointer]:
                    - generic [ref=e678]: 
            - row " pimuser08421578 ESS Raj ravi Enabled  " [ref=e680]:
              - cell "" [ref=e681]:
                - generic [ref=e684] [cursor=pointer]:
                  - checkbox "" [ref=e685]
                  - generic [ref=e687]: 
              - cell "pimuser08421578" [ref=e688]:
                - generic [ref=e689]: pimuser08421578
              - cell "ESS" [ref=e690]:
                - generic [ref=e691]: ESS
              - cell "Raj ravi" [ref=e692]:
                - generic [ref=e693]: Raj ravi
              - cell "Enabled" [ref=e694]:
                - generic [ref=e695]: Enabled
              - cell " " [ref=e696]:
                - generic [ref=e697]:
                  - button "" [ref=e698] [cursor=pointer]:
                    - generic [ref=e699]: 
                  - button "" [ref=e700] [cursor=pointer]:
                    - generic [ref=e701]: 
            - row " playwright_user36370 ESS Mark Smith Enabled  " [ref=e703]:
              - cell "" [ref=e704]:
                - generic [ref=e707] [cursor=pointer]:
                  - checkbox "" [ref=e708]
                  - generic [ref=e710]: 
              - cell "playwright_user36370" [ref=e711]:
                - generic [ref=e712]: playwright_user36370
              - cell "ESS" [ref=e713]:
                - generic [ref=e714]: ESS
              - cell "Mark Smith" [ref=e715]:
                - generic [ref=e716]: Mark Smith
              - cell "Enabled" [ref=e717]:
                - generic [ref=e718]: Enabled
              - cell " " [ref=e719]:
                - generic [ref=e720]:
                  - button "" [ref=e721] [cursor=pointer]:
                    - generic [ref=e722]: 
                  - button "" [ref=e723] [cursor=pointer]:
                    - generic [ref=e724]: 
            - row " playwright_user80674 ESS Mark Smith Enabled  " [ref=e726]:
              - cell "" [ref=e727]:
                - generic [ref=e730] [cursor=pointer]:
                  - checkbox "" [ref=e731]
                  - generic [ref=e733]: 
              - cell "playwright_user80674" [ref=e734]:
                - generic [ref=e735]: playwright_user80674
              - cell "ESS" [ref=e736]:
                - generic [ref=e737]: ESS
              - cell "Mark Smith" [ref=e738]:
                - generic [ref=e739]: Mark Smith
              - cell "Enabled" [ref=e740]:
                - generic [ref=e741]: Enabled
              - cell " " [ref=e742]:
                - generic [ref=e743]:
                  - button "" [ref=e744] [cursor=pointer]:
                    - generic [ref=e745]: 
                  - button "" [ref=e746] [cursor=pointer]:
                    - generic [ref=e747]: 
            - row " playwright_user89310 ESS Mark Smith Enabled  " [ref=e749]:
              - cell "" [ref=e750]:
                - generic [ref=e753] [cursor=pointer]:
                  - checkbox "" [ref=e754]
                  - generic [ref=e756]: 
              - cell "playwright_user89310" [ref=e757]:
                - generic [ref=e758]: playwright_user89310
              - cell "ESS" [ref=e759]:
                - generic [ref=e760]: ESS
              - cell "Mark Smith" [ref=e761]:
                - generic [ref=e762]: Mark Smith
              - cell "Enabled" [ref=e763]:
                - generic [ref=e764]: Enabled
              - cell " " [ref=e765]:
                - generic [ref=e766]:
                  - button "" [ref=e767] [cursor=pointer]:
                    - generic [ref=e768]: 
                  - button "" [ref=e769] [cursor=pointer]:
                    - generic [ref=e770]: 
            - row " rachel.green2 ESS Rachel Green Enabled  " [ref=e772]:
              - cell "" [ref=e773]:
                - generic [ref=e776] [cursor=pointer]:
                  - checkbox "" [ref=e777]
                  - generic [ref=e779]: 
              - cell "rachel.green2" [ref=e780]:
                - generic [ref=e781]: rachel.green2
              - cell "ESS" [ref=e782]:
                - generic [ref=e783]: ESS
              - cell "Rachel Green" [ref=e784]:
                - generic [ref=e785]: Rachel Green
              - cell "Enabled" [ref=e786]:
                - generic [ref=e787]: Enabled
              - cell " " [ref=e788]:
                - generic [ref=e789]:
                  - button "" [ref=e790] [cursor=pointer]:
                    - generic [ref=e791]: 
                  - button "" [ref=e792] [cursor=pointer]:
                    - generic [ref=e793]: 
            - row " raju@office.com ESS Raju M Enabled  " [ref=e795]:
              - cell "" [ref=e796]:
                - generic [ref=e799] [cursor=pointer]:
                  - checkbox "" [ref=e800]
                  - generic [ref=e802]: 
              - cell "raju@office.com" [ref=e803]:
                - generic [ref=e804]: raju@office.com
              - cell "ESS" [ref=e805]:
                - generic [ref=e806]: ESS
              - cell "Raju M" [ref=e807]:
                - generic [ref=e808]: Raju M
              - cell "Enabled" [ref=e809]:
                - generic [ref=e810]: Enabled
              - cell " " [ref=e811]:
                - generic [ref=e812]:
                  - button "" [ref=e813] [cursor=pointer]:
                    - generic [ref=e814]: 
                  - button "" [ref=e815] [cursor=pointer]:
                    - generic [ref=e816]: 
            - row " txauto_1783409361956 Admin Rosalia Abshire Enabled  " [ref=e818]:
              - cell "" [ref=e819]:
                - generic [ref=e822] [cursor=pointer]:
                  - checkbox "" [ref=e823]
                  - generic [ref=e825]: 
              - cell "txauto_1783409361956" [ref=e826]:
                - generic [ref=e827]: txauto_1783409361956
              - cell "Admin" [ref=e828]:
                - generic [ref=e829]: Admin
              - cell "Rosalia Abshire" [ref=e830]:
                - generic [ref=e831]: Rosalia Abshire
              - cell "Enabled" [ref=e832]:
                - generic [ref=e833]: Enabled
              - cell " " [ref=e834]:
                - generic [ref=e835]:
                  - button "" [ref=e836] [cursor=pointer]:
                    - generic [ref=e837]: 
                  - button "" [ref=e838] [cursor=pointer]:
                    - generic [ref=e839]: 
    - generic [ref=e841]:
      - paragraph [ref=e842]: OrangeHRM OS 5.8
      - paragraph [ref=e843]:
        - text: © 2005 - 2026
        - link "OrangeHRM, Inc" [ref=e844] [cursor=pointer]:
          - /url: http://www.orangehrm.com
        - text: . All rights reserved.
```

# Test source

```ts
  1   | import { test, expect, Page } from '@playwright/test';
  2   | 
  3   | const BASE_URL = 'https://opensource-demo.orangehrmlive.com';
  4   | const ADMIN_USER = 'Admin';
  5   | const ADMIN_PASSWORD = 'admin123';
  6   | 
  7   | async function login(page: Page) {
  8   |   await page.goto(`${BASE_URL}/web/index.php/auth/login`);
  9   |   await page.fill('input[name="username"]', ADMIN_USER);
  10  |   await page.fill('input[name="password"]', ADMIN_PASSWORD);
  11  |   await page.click('button[type="submit"]');
  12  |   await page.waitForURL(`${BASE_URL}/**`);
  13  | }
  14  | 
  15  | async function navigateToModule(page: Page, moduleUrl: string) {
  16  |   await page.goto(`${BASE_URL}${moduleUrl}`);
  17  |   await page.waitForLoadState('networkidle');
  18  | }
  19  | 
  20  | // ═════════════════════════════════════════════════════════════════════════
  21  | // MODULE 1: ADMIN - USER MANAGEMENT (12 Sub-functions)
  22  | // ═════════════════════════════════════════════════════════════════════════
  23  | 
  24  | test.describe('ADMIN: User Management', () => {
  25  |   test.beforeEach(async ({ page }) => {
  26  |     await login(page);
  27  |     await navigateToModule(page, '/web/index.php/admin/viewAdminModule');
  28  |   });
  29  | 
  30  |   test('WF-1.1: View all system users list', async ({ page }) => {
  31  |     await expect(page.locator('text=System Users')).toBeVisible();
  32  |     const rows = page.locator('table tbody tr');
> 33  |     expect(await rows.count()).toBeGreaterThan(0);
      |                                ^ Error: expect(received).toBeGreaterThan(expected)
  34  |   });
  35  | 
  36  |   test('WF-1.2: Search users by username field', async ({ page }) => {
  37  |     const searchInput = page.locator('input[placeholder*="Username"], input[name="username"]').first();
  38  |     if (await searchInput.isVisible()) {
  39  |       await searchInput.fill('Admin');
  40  |       await page.click('button:has-text("Search")');
  41  |       expect(await page.locator('table tbody tr').count()).toBeGreaterThan(0);
  42  |     }
  43  |   });
  44  | 
  45  |   test('WF-1.3: Filter by role dropdown (Admin/ESS)', async ({ page }) => {
  46  |     const selects = page.locator('select');
  47  |     if (await selects.first().isVisible()) {
  48  |       await selects.first().selectOption('1');
  49  |       await page.click('button:has-text("Search")');
  50  |     }
  51  |   });
  52  | 
  53  |   test('WF-1.4: Filter by status (Enabled/Disabled)', async ({ page }) => {
  54  |     const statusSelect = page.locator('select').nth(1);
  55  |     if (await statusSelect.isVisible()) {
  56  |       await statusSelect.selectOption('Enabled');
  57  |     }
  58  |   });
  59  | 
  60  |   test('WF-1.5: Edit user button functionality', async ({ page }) => {
  61  |     const editBtn = page.locator('button[aria-label*="Edit"], [title*="Edit"]').first();
  62  |     if (await editBtn.isVisible()) {
  63  |       expect(await editBtn.isVisible()).toBeTruthy();
  64  |     }
  65  |   });
  66  | 
  67  |   test('WF-1.6: Delete user button visibility', async ({ page }) => {
  68  |     const deleteBtn = page.locator('button[aria-label*="Delete"], [title*="Delete"]').first();
  69  |     if (await deleteBtn.isVisible()) {
  70  |       expect(await deleteBtn.isVisible()).toBeTruthy();
  71  |     }
  72  |   });
  73  | 
  74  |   test('WF-1.7: Reset filters button', async ({ page }) => {
  75  |     const resetBtn = page.locator('button:has-text("Reset")');
  76  |     await expect(resetBtn).toBeVisible();
  77  |   });
  78  | 
  79  |   test('WF-1.8: Add new user button', async ({ page }) => {
  80  |     const addBtn = page.locator('button:has-text("Add")');
  81  |     await expect(addBtn).toBeVisible();
  82  |   });
  83  | 
  84  |   test('WF-1.9: Username column sortable', async ({ page }) => {
  85  |     await expect(page.locator('th:has-text("Username")')).toBeVisible();
  86  |   });
  87  | 
  88  |   test('WF-1.10: User role column sortable', async ({ page }) => {
  89  |     await expect(page.locator('th:has-text("User Role")')).toBeVisible();
  90  |   });
  91  | 
  92  |   test('WF-1.11: Employee name column sortable', async ({ page }) => {
  93  |     await expect(page.locator('th:has-text("Employee Name")')).toBeVisible();
  94  |   });
  95  | 
  96  |   test('WF-1.12: Status column sortable', async ({ page }) => {
  97  |     await expect(page.locator('th:has-text("Status")')).toBeVisible();
  98  |   });
  99  | });
  100 | 
  101 | // ═════════════════════════════════════════════════════════════════════════
  102 | // MODULE 2: PIM - EMPLOYEE LIST (15 Sub-functions)
  103 | // ═════════════════════════════════════════════════════════════════════════
  104 | 
  105 | test.describe('PIM: Employee List', () => {
  106 |   test.beforeEach(async ({ page }) => {
  107 |     await login(page);
  108 |     await navigateToModule(page, '/web/index.php/pim/viewEmployeeList');
  109 |   });
  110 | 
  111 |   test('WF-2.1: View employee list with 133 records', async ({ page }) => {
  112 |     await expect(page.locator('text=Records Found')).toBeVisible({ timeout: 10000 });
  113 |   });
  114 | 
  115 |   test('WF-2.2: Search by employee name', async ({ page }) => {
  116 |     const searchInput = page.locator('input[placeholder*="Employee Name"]').first();
  117 |     if (await searchInput.isVisible()) {
  118 |       await searchInput.fill('Alisa');
  119 |       await page.click('button:has-text("Search")');
  120 |     }
  121 |   });
  122 | 
  123 |   test('WF-2.3: Search by employee ID', async ({ page }) => {
  124 |     const idInput = page.locator('input[placeholder*="Employee ID"]').first();
  125 |     if (await idInput.isVisible()) {
  126 |       await idInput.fill('7369');
  127 |     }
  128 |   });
  129 | 
  130 |   test('WF-2.4: Filter by employment status', async ({ page }) => {
  131 |     const statusSelect = page.locator('select').filter({ has: page.locator('option') }).first();
  132 |     if (await statusSelect.isVisible()) {
  133 |       const options = statusSelect.locator('option');
```