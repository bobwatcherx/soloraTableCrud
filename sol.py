# INSTALL PANDAS IN YOU PC WITH pip install pandas
import pandas as pd
from solara import *
import dataclasses
from typing import Any,Dict,Optional,cast


# CREATE DATA CLASS FAKE NAME AND AGE
@dataclasses.dataclass(frozen=True)
class Fakedata:
    name:str
    age:int

mysample = pd.DataFrame()



@solara.component
def Page():
    name,set_name = use_state("")
    age,set_age = use_state(0)
    mycell,set_mycell = use_state(cast(Dict[str,Any],{}))
    idselect = use_reactive(0)
    # AND NOW I CREATE FAKE DATA FOR MYDATA
    mydata = use_reactive([
        Fakedata("jul",12),
        Fakedata("dw",34),
        Fakedata("grr",54),
        ])



    def youactioncell(column,row_index):
        # NOW IF YOU CLICK SELECT IN TABLE THEN GET 
        # ROW DATA  LIKE NAME AND AGE
        set_mycell(dict(column=column,row_index=row_index))
        # AND NOW SET TO TEXT FIELD NAME AND AGE 
        for i,x in enumerate(mydata.value):
            if i == row_index:
                set_name(x.name)
                set_age(x.age)
                # AND GET ID WHEN YOU SELECT TABLE 
                idselect.value = row_index
                print("you select",idselect)




    def updatedata():
        # AND NOW UPDATE dATA
        myeditdata = mydata.value.copy()
        # AND NOW LOOP AND FIND ID IF FOUND THEN CHANGE VALUE
        for i,x in enumerate(mydata.value):
            if i == idselect.value:
                myeditdata[idselect.value] = Fakedata(name,age)
                print(x)
        mydata.value = myeditdata
        # AND CLEAAR INPUT
        set_name("")
        set_age("")


    def deletedata():
        if idselect.value < len(mydata.value):
            mydeldata = mydata.value.copy()
            mydeldata.pop(idselect.value)
            mydata.value = mydeldata
            set_name("")
            set_age(0)


    def addnewdata():
        # AND NOW ADD DATA TO TABLE
        newdata = Fakedata(name,int(age))
        # AND PUSH TO mydata.value
        mydata.value = [*mydata.value,newdata]

        # AND CLEAR INPUT
        set_name("")
        set_age("")



    mycellactions = [solara.CellAction(icon="mdi-account-arrow-right",
        name="select this data",
        on_click=youactioncell

        )]
    mysample = pd.DataFrame.from_records([dataclasses.asdict(x) for x in mydata.value])



    with Column(align="center"):
        Markdown("TABLE CRUD")
        InputText(label="name",value=name,
            on_value=set_name
            )
        InputText(label="age",value=age,
            on_value=set_age
            )
        with Row(justify="space-around"):
            Button("edit",color="primary",
                on_click=updatedata
                )
            Button("delete",color="red",
                on_click=deletedata
                )
            Button("add new",color="green",
                on_click=addnewdata
                )
        DataFrame(mysample,cell_actions=mycellactions)
