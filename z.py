def get_item(cadena):
    retornar=""
    temp=0
    bloqueo='collectionitem="'
    for i in range(len(cadena)):
        if(temp==len(bloqueo)):
            if(cadena[i]=='"'):
                if(len(retornar)==0): 
                    temp=0
                    continue
                else: return retornar
            retornar+=cadena[i]  
        else:
            if(cadena[i]==bloqueo[temp]): temp+=1
            else: temp=0

def extraer_fecha(cadena):
    temp=""
    for i in range(len(cadena)-1,-1,-1):
        if(cadena[i]=="_"): return temp
        temp=cadena[i]+temp

a="""<div class="collapsablePanel" collectionitem="soccer_copa-america-2024_matches_2024-06-27"><div class="collapsableHeader" collapsed="true" data-tap-recogniser="true"><div class="arrow iconHolder"><div class="arrowIcon icon-arrow-right"></div></div><div class="titleTextWrapper"><div class="titleText">ju. 27 jun.</div><div class="subTitle"></div></div><div class="Message"></div><div class="marketFilteringHeaderContainer empty" data-container="SpinSport.Application.mainLayout.firstRowContainer.subcategoryLayout.SubcategoryWidget.SubcategoryEventListWidget[soccer_copa-america-2024, EVENT_FILTER_FIXTURES].EventTableListWidget[soccer_copa-america-2024_matches, soccer_copa-america-2024_matches].MarketFilteringWidgetContainer[soccer_copa-america-2024_matches_2024-06-27]"></div></div><div class="collapsableContent empty" collapsed="true" data-container="SpinSport.Application.mainLayout.firstRowContainer.subcategoryLayout.SubcategoryWidget.SubcategoryEventListWidget[soccer_copa-america-2024, EVENT_FILTER_FIXTURES].EventTableListWidget[soccer_copa-america-2024_matches, soccer_copa-america-2024_matches].EventListWidgetContainer[soccer_copa-america-2024_matches_2024-06-27]"></div></div>"""

#print(get_item(a))

print(extraer_fecha("soccer_copa-america-2024_matches_2024-06-23"))