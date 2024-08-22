document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose2').addEventListener('click', compose_email);


  // By default, load the inbox
  load_mailbox('inbox');

  document.querySelector('#compose-form').addEventListener('submit', send_email);
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#message-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

async function load_mailbox(mailbox) {

  const emailsContainer = document.getElementById('emails-view');
  emailsContainer.innerHTML = ''; // Clear previous content if any

  // Show the mailbox name
  const mailboxName = mailbox.charAt(0).toUpperCase() + mailbox.slice(1);
  document.querySelector('#email-type').innerHTML = `<i class="fa fa-${mailboxIcon(mailbox)}"></i> ${mailboxName}`;

  // Create the wrapping <div class="table-responsive">
  const tableResponsiveDiv = document.createElement('div');
  tableResponsiveDiv.classList.add('table-responsive');

  // Create the <table> element
  const table = document.createElement('table');
  table.classList.add('table');

  // Create the <tbody> element
  const tbody = document.createElement('tbody');

  // Append the <tbody> to the <table>
  table.appendChild(tbody);

  // Append the <table> to the <div class="table-responsive">
  tableResponsiveDiv.appendChild(table);

  // Append the entire structure to the emailsContainer
  emailsContainer.appendChild(tableResponsiveDiv);

  // Fetch email data and populate the table rows
  try {
    const response = await fetch(`/emails/${mailbox}`);
    const emails = await response.json();

    emails.forEach(email => {
      if (mailbox === 'sent') {
        const emailDiv = document.createElement('tr');
        emailDiv.setAttribute('onclick', `send_view(${email.id})`);
        emailDiv.classList.add('read');
        emailDiv.innerHTML = `
          <td class="name">${email.recipients[0]}</td>
          <td class="subject">${email.subject}</td>
          <td class="time">${email.timestamp}</td>
        `;
        tbody.appendChild(emailDiv);
      } else if (mailbox === 'archive') {
        const emailDiv = document.createElement('tr');
        emailDiv.setAttribute('onclick', `view(${email.id})`);
        if (!email.read)  {
          emailDiv.innerHTML = `
            <td><a onclick="unarchive(event, ${email.id})"><i class="fa fa-folder"></i></a></td>
            <td class="name">${email.sender}</td>
            <td class="subject">${email.subject}</td>
            <td class="time">${email.timestamp}</td>
          `;
          tbody.appendChild(emailDiv);
        } else {
          const emailDiv = document.createElement('tr');
          emailDiv.setAttribute('onclick', `view(${email.id})`);
          emailDiv.classList.add('read');
          emailDiv.innerHTML = `
            <td><a onclick="unarchive(event, ${email.id})"><i class="fa fa-folder"></i></a></td>
            <td class="name">${email.sender}</td>
            <td class="subject">${email.subject}</td>
            <td class="time">${email.timestamp}</td>
          `;
          tbody.appendChild(emailDiv);
        }
      } else {
        const emailDiv = document.createElement('tr');
        emailDiv.setAttribute('onclick', `view(${email.id})`);
        if (!email.read) {
          emailDiv.innerHTML = `
            <td><a onclick="archive(event, ${email.id})"><i class="fa fa-folder"></i></a></td>
            <td class="name">${email.sender}</td>
            <td class "subject">${email.subject}</td>
            <td class="time">${email.timestamp}</td>
          `;
          tbody.appendChild(emailDiv);
        } else {
          const emailDiv = document.createElement('tr');
          emailDiv.setAttribute('onclick', `view(${email.id})`);
          emailDiv.classList.add('read');
          emailDiv.innerHTML = `
            <td><a onclick="archive(event, ${email.id})"><i class="fa fa-folder"></i></a></td>
            <td class="name">${email.sender}</td>
            <td class="subject">${email.subject}</td>
            <td class="time">${email.timestamp}</td>
          `;
          tbody.appendChild(emailDiv);
        }
      }

    });
  } catch (error) {
    console.error('Error fetching and displaying emails:', error);
  }

  // Show the mailbox and hide other views
document.querySelector('#emails-view').style.display = 'block';
document.querySelector('#compose-view').style.display = 'none';
document.querySelector('#message-view').style.display = 'none';


}

function mailboxIcon(mailbox) {
  switch (mailbox) {
    case 'inbox':
      return 'inbox';
    case 'sent':
      return 'mail-forward';
    case 'archived':
      return 'folder';
    default:
      return 'pencil-square-o';
  }
}


async function send_email(event) {
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  const response = await fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  });

  const result = await response.json();
  console.log(result);

  load_mailbox('sent');
}

async function read(id){
  await fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });
}

async function archive(event, id){
  // Prevent the click event from bubbling up to the parent element (view anchor)
  event.stopPropagation();

  await fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  });
  load_mailbox('inbox');
}

async function unarchive(event, id){
  // Prevent the click event from bubbling up to the parent element (view anchor)
  event.stopPropagation();

  await fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  });
  load_mailbox('archive');
}

function modal_close() {
  document.querySelector('#message-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
}

async function view(id){

  const emailContainer = document.getElementById('message-view');
  emailContainer.innerHTML = ''; // Clear previous content if any

  await fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    try {
      if (!email.read) {
        read(id);
      }
    } catch (error) {
      console.error('Error fetching and displaying emails:', error);
    }

    emailContainer.innerHTML = `
      <div class="modal-wrapper">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header bg-blue">
                    <button class="close" onclick="modal_close()" aria-hidden="true">×</button>
                    <h4 class="modal-title"><i class="fa fa-envelope"></i> ${email.sender}</h4>
                </div>
                <div>
                    <div class="modal-body">
                        <div class="form-group">
                            <p> ${email.subject} </p>
                        </div>
                        <div class="form-group">
                            <p> ${email.timestamp} </p>
                        </div>
                        <div class="form-group">
                            <p style="height: 120px; overflow-y: scroll;"> ${email.body}</p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button onclick="re_compose_email(${email.id})" class="btn btn-primary pull-right"><i class="fa fa-envelope"></i> Replay</button>
                    </div>
                </div>
            </div>
        </div>
      </div>
    `;
  });
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#message-view').style.display = 'block';

}

async function send_view(id){

  const emailContainer = document.getElementById('message-view');
  emailContainer.innerHTML = ''; // Clear previous content if any

  await fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    emailContainer.innerHTML = `
      <div class="modal-wrapper">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header bg-blue">
                    <button class="close" onclick="modal_close()" aria-hidden="true">×</button>
                    <h4 class="modal-title"><i class="fa fa-envelope"></i> ${email.recipients}</h4>
                </div>
                <div>
                    <div class="modal-body">
                        <div class="form-group">
                            <p> ${email.subject} </p>
                        </div>
                        <div class="form-group">
                            <p> ${email.timestamp} </p>
                        </div>
                        <div class="form-group">
                            <p style="height: 120px; overflow-y: scroll;"> ${email.body}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      </div>
    `;
  });
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#message-view').style.display = 'block';

}

async function re_compose_email(id) {
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  try {
    const response = await fetch(`/emails/${id}`);
    const email = await response.json();

    // Load data into composition fields
    let subject = email.subject;

    // Check if the subject starts with "Re:"; if not, prepend it
    if (!subject.startsWith('Re: ')) {
      subject = `Re: ${subject}`;
    }

    document.querySelector('#compose-subject').value = subject;
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#message-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
  } catch (error) {
    console.error('Error fetching and displaying email for re-composition:', error);
  }
}
