# Go through each file in a given directory

import os

dir_interface   = 'C:/Users/aalee/proj/dev/UVMF_2022.3_ALTAI/templates/python/template_files/interface_templates'
dir_bench       = 'C:/Users/aalee/proj/dev/UVMF_2022.3_ALTAI/templates/python/template_files/bench_templates'
dir_environment = 'C:/Users/aalee/proj/dev/UVMF_2022.3_ALTAI/templates/python/template_files/environment_templates'

directories = [dir_interface, dir_bench, dir_environment]

#output_dir = 'C:/Users/aalee/proj/dev/UVMF_2022.3_ALTAI/templates/python/template_files/interface_templates'





# description = """

# /****************************************************************************** 
# * Filename: {wline} 
# * Author: {{user}} 
# * Year: {{year}}   
# ********************************************************************************/
# """
for dir in directories:
    for filename in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, filename)):
            filename = os.path.join(dir, filename)
            mod_lines = []
            #output_filepath = os.path.join(output_dir, filename)
            #print("DBGALEEN", filename)
        # Go throught each line in a given file
        with open (filename, 'r') as FH:
            for line in FH:
                           
                # Going through only non-empty (???)
                #print("DBGALEEN2", line)
                words = line.split()           
                # print that line
                for word in words:
                    # Find the line that matches pattern "fname" in the file (???)
                    if(word == "fname"):
                        # Make sure you remove the whitespaces (???)
                        wline = line.replace(' ','')
                        wline = wline[12:-4]
                        #print(wline)
                mod_lines.append(line)
                if line.strip() == "{% block description %}":
                    
                    
                    if ('.f' and ".svh" and ".F" and ".sv") not in wline:
                        print('filename_IF_debug: '+ wline)
                        mod_lines.append(f"""#****************************************************************************** \n# Filename: {wline} \n# Author: {{{{user}}}} \n# Year: {{{{year}}}}   \n#*******************************************************************************/\n""")
       
                       # mod_lines.append(f"""/****************************************************************************** \n* Filename: {wline} \n* Author: {{{{user}}}} \n* Year: {{{{year}}}}   \n********************************************************************************/\n""")
                    else:
                        print('filename_ELSE_debug: '+ wline)
                        mod_lines.append(f"""/****************************************************************************** \n* Filename: {wline} \n* Author: {{{{user}}}} \n* Year: {{{{year}}}}   \n********************************************************************************/\n""")
                    
                        #mod_lines.append(f"""#****************************************************************************** \n# Filename: {wline} \n# Author: {{{{user}}}} \n# Year: {{{{year}}}}   \n#*******************************************************************************/\n""")
        
        with open(filename, 'w') as FH:
                FH.writelines(mod_lines)

    

        # Go through the lines again
        # Fine the line that matches pattern description
    
        # open the filename with write permision
        #/****************************************************************************** 
        #* Filename: {{bench_location}}/docs/interfaces.csv 
        #* Author: {{user}} 
        #* Year: {{year}}   
        #********************************************************************************/








