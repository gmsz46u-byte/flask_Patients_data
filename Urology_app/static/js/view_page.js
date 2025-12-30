let radiobtn2 = document.getElementById('btnradio2');
// function to extend pt card in search_one page
function extend_name(element) {
    radiobtn2.click();
    let parentCover = element.parentElement; // use let not const(raises error)  كسم const
    let name_span = parentCover.children[0].children[1];
    let pt_name = name_span.textContent;
    console.log(pt_name)
    // prepare element to handle all data to view in search_page as card 
    const name_viewer = document.createElement('div')
    name_viewer.classList.add('search-one-name','card' ,'bg-white', 'rad-10', 'p-rel','mb-10')
    // creating deleting & editing btns >> VIP !!!! btn must be appended after all paragraphs to be the last child
    let delete_btn = document.createElement("button");
    delete_btn.setAttribute("onclick","delete_name(this)");
    delete_btn.classList.add("delete-btn");
    let editing_btn = document.createElement("button");
    editing_btn.setAttribute("onclick","to_editing_page(this)");
    editing_btn.classList.add("editing-btn");
    // starting jquery to send data to python file and receive response
    let name = {"name_to_search":pt_name}; 
    $.ajax({
            url:"/view_page",
            type:'POST',
            contentType:'application/json; charset=UTF-8', // must be application/json >> only 'json' not working
            // contentType:"application/x-www-form-urlencoded; charset=UTF-8", // must be application/json >> only 'json' not working
            data: JSON.stringify(name),
            success:function(response) { // console.log(response) // response is equal to {age: 44, complaint: 'gfgf', gender: 'male', labs: 'gdfgdf', name: 'ahmed', …}age: 44complaint: "gfgf"gender: "male"labs: "gdfgdf"name: "ahmed"operation: "TURP"pmh: "CKD&NIDDM"psh: "gdfgdf"rads:"gfdgdf"
                // for (i==0;i<Object.value(response).length;i++) {}
                pt_hx = `For : ${response.operation} .;;\
                ${response.name} ;;\
                A ${response.age} year old ${response.gender} pt;;\
                presented with ${response.complaint} .;;\
                pt has ${response.pmh} .;;\
                pt also had ${response.psh} .;;\
                Relevant Labs : ${response.labs} .;;\
                Relevant Rads : ${response.rads} .;;`
                text_list = pt_hx.split(";;");
                // replace content of name_viewer by removing prevoius content
                for (let i = 0 ; i<text_list.length ; i++) {
                    let p = document.createElement('p');
                    p.textContent = text_list[i].trim();
                    // then adding my element
                    name_viewer.appendChild(p);
                }
                // add btns to div
                name_viewer.append(delete_btn,editing_btn)
                // add to main-content
                document.querySelector('.main-content-container').appendChild(name_viewer)
            }})
};

// fuction to start delete popover to delete patient from db
function delete_name(element) {
    // showing popover with submit button 
    // setting backdrop
    document.getElementById('manual-backdrop').style.display = 'block';
    // setting popover
    let delete_popover = document.createElement('div');
    delete_popover.textContent = 'This will delete pt from db permenantly.\nAre you sure you want to proceed?';
    let my_attrs = document.createAttribute('popover');
    delete_popover.setAttributeNode(my_attrs);
    delete_popover.classList.add('delete-popover')
    // setting submit btn
    let submit_btn = document.createElement('button');
    submit_btn.setAttribute('onclick','submit_delete()');
    submit_btn.classList.add('btn' ,'btn-outline-info','c-red');
    submit_btn.textContent = 'Submit';
    // setting dismiss btn
    let dismiss_btn = document.createElement('button');
    dismiss_btn.setAttribute('onclick','dismiss_deleting()');
    dismiss_btn.classList.add('btn' ,'btn-outline-info','c-red');
    dismiss_btn.textContent = 'Cancel';
    // searching db
    const parentCard =element.parentElement;
    const name_p =parentCard.children[1];
    pt_name = name_p.textContent;
    let name =  {'name':pt_name};
    $.ajax({
    url:'/delete_patient',
    type:'POST',
    contentType:'application/json; charset=UTF-8',
    data: JSON.stringify(name),
    success:function(response) {
        console.log(response)
        delete_popover.appendChild(submit_btn);
        delete_popover.appendChild(dismiss_btn);
        document.body.appendChild(delete_popover);
    }
})
    

}

// function to submit delete pt from db
function submit_delete() {
    // remove popover and hide backdrop
    let delete_popover = document.querySelector('.delete-popover')
    delete_popover.remove();
    document.getElementById('manual-backdrop').style.display = 'none';
    // delete pt from db
    $.ajax({
        url:'/delete_patient',
        type:'POST',
        contentType:'application/json',
        data:JSON.stringify({'order':'submit delete'}),
        success:function() {
            const success_alert = `<div class="alert alert-success" role="alert">Patient has been deleted successfully</div>`;
            const my_container = document.querySelector('.main-content-container');
            my_container.insertAdjacentHTML('afterbegin',success_alert);
        },
        error:function() {
            const failed_alert = `<div class="alert alert-danger" role="alert">Error with process ,please check data carefully!! </div>`;
            const my_container = document.querySelector('.main-content-container');
            my_container.insertAdjacentHTML('afterbegin',failed_alert);
        },
        complete:function() {
            // this functin should be transfered to success block
            $.ajax({
                url:'/backup_data',
                type:'POST',
                contentType:'application/json',
            })
        }
    })
}

// fuction to dismiss deleting process
function dismiss_deleting() {
    // hide backdrop
    document.getElementById('manual-backdrop').style.display = 'none';
    //remove name_to_delete at backend
    $.ajax({
        url:'/dismiss_deleting',
        type:'POST',
        contentType:'application/json; charset=UTF-8',
        success:function() {
            // remove parent popover
            let popover = document.querySelector('.delete-popover')
            popover.remove();
        }
    })
}

// function to go to editing page on click on editing icon in search one card
function to_editing_page(element) {
    console.log(element)
    console.log(this)
    let parentCard = element.parentElement;
    const p_2 = parentCard.children[1];
    const name_to_edit = p_2.textContent;
    let name = {'name_to_store':name_to_edit};
    // sotre name in flask variable
    $.ajax({
        url:'/switch_pgs',
        type:'POST',
        contentType:'application/json',
        data:JSON.stringify(name),
    })
    // redirect to editing page using js
    window.location.href = 'editing_page';
}

// when radiobtn1 is clicked load html for view_all // when radionbtn2 load search_one elemnet 
$(window).ready(function() {
    $('.btn-check').click(function(){
        $.ajax({
            url:'/view_check',
            type:'POST',
            contentType:'application/json',
            data:{'id':(this).id},  // this.id returs btn id
            success:function(response) { // response is of type string
                // to convert string into html before appendChild
                const parser = new DOMParser();
                const htmlDoc = parser.parseFromString(response,'text/html');// this creates full html with body containg target html
                const responseElement = htmlDoc.body.children[0]; // targets my element                // replacing current element with new one in main-content
                document.querySelector('.main-content-container').replaceChildren(responseElement);
            }
        })
    })
});


// function to iterate pages in view all patients section
function iter_pages(element) {
    let requested_page = element.getAttribute('title');
    $.ajax({
        url:'/view_check',
        type:'GET',
        contentType:'application/json',
        data:{'page':requested_page},
        success:function(response){
            const parser = new DOMParser();
            const dochtml = parser.parseFromString(response,'text/html')
            const new_cards_wrapper = dochtml.body.children[0].children[0].children; // reched by trial to get cards-wrapper
            console.log(new_cards_wrapper);
            const cards_container = document.querySelector('.cards-container')
            cards_container.replaceChildren(new_cards_wrapper[0]); // replace cards with new content
        }
    })
}


// fucntion to search one pt data using input text
$(document.querySelector('.main-content-container')).on("change",".view-pt-data",function(){
    const name_to_search = this.value;
    const name_viewer = document.createElement("div");
    name_viewer.classList.add('search-one-name','card' ,'bg-white', 'rad-10', 'p-rel','mb-10');
    // creating deleting & editing btns >> VIP !!!! btn must be appended after all paragraphs to be the last child
    let delete_btn = document.createElement("button");
    delete_btn.setAttribute("onclick","delete_name(this)");
    delete_btn.classList.add("delete-btn");
    let editing_btn = document.createElement("button");
    editing_btn.setAttribute("onclick","to_editing_page(this)");
    editing_btn.classList.add("editing-btn");
    let name = {'name_to_search':name_to_search};
    $.ajax({
        url:"/view_page",
        type:'POST',
        contentType:'application/json', // must be application/json >> only 'json' not working
        data: JSON.stringify(name),
        success:function(response) { // console.log(response) // response is equal to {age: 44, complaint: 'gfgf', gender: 'male', labs: 'gdfgdf', name: 'ahmed', …}age: 44complaint: "gfgf"gender: "male"labs: "gdfgdf"name: "ahmed"operation: "TURP"pmh: "CKD&NIDDM"psh: "gdfgdf"rads:"gfdgdf"
            // for (i==0;i<Object.value(response).length;i++) {}
            if (response && Object.keys(response).length > 0) {
            pt_hx = `For : ${response.operation} .;;\
            ${response.name} ;;\
            A ${response.age} year old ${response.gender} pt;;\
            presented with ${response.complaint} .;;\
            pt has ${response.pmh} .;;\
            pt also had ${response.psh} .;;\
            Relevant Labs : ${response.labs} .;;\
            Relevant Rads : ${response.rads}.;;`
            text_list = pt_hx.split(";;");
            // replace content of name_viewer by removing prevoius content
            for (let i = 0 ; i<text_list.length ; i++) {
                let p = document.createElement('p');
                p.textContent = text_list[i].trim();
                // then adding my element
                name_viewer.appendChild(p);
            }
            // adding btns
            name_viewer.append(delete_btn,editing_btn);
            // add to main-content
            document.querySelector('.main-content-container').appendChild(name_viewer);
        } else {
            const failed_alert = `<div class="alert alert-danger" role="alert">Error with process ,No such pt in db!! </div>`;
            const my_container = document.querySelector('.main-content-container');
            my_container.insertAdjacentHTML('afterbegin',failed_alert);
        }
    }})

});
