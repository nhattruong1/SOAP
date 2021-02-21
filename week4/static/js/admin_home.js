let question_id = 0;
function addQuestion(){
    let quizz_name = document.getElementById('content_quizz').value;
    let list_question = document.getElementById('list_question');
    if(!quizz_name){
        alert('Phải đặt tên cho bài trắc nghiệm')
    }else if(question_id === 20){
        alert('Chỉ được tạo tối đa 20 câu hỏi')
    } else {
           question_id ++;
           let object_question = {
            name : '// Nội dung câu hỏi',
            answer: [
                {
                    content : '// Nội dung đáp án A',
                    correct: '// false là sai, true là đúng'
                },
                {
                    content : '// Nội dung đáp án A',
                    correct: '// false là sai, true là đúng'
                },
                {
                    content : '// Nội dung đáp án A',
                    correct: '// false là sai, true là đúng'
                },
                {
                    content : '// Nội dung đáp án A',
                    correct: '// false là sai, true là đúng'
                },
            ]
        };

        let html_question = `
            <div>
              <label for="question"><b>Câu ${question_id}: </b></label>
              <textarea class="form-control" name="question" style="height: 550px !important;margin-bottom: 5px">${JSON.stringify(object_question, null, 4)}</textarea>
            </div>
        `;
        list_question.innerHTML += html_question;
    }
}

function save(){
    let list_question = document.getElementsByName('question');
    let quizz_name = document.getElementById('content_quizz').value;
    let subject_id = document.getElementById('subject_id').textContent;
    let object_quizz = {
        name: quizz_name,
        subject_id: subject_id,
        array_question: []
    }
    if(list_question.length === 0 || !quizz_name){
        if(list_question.length === 0){
            alert('Chưa có câu hỏi!')
        }else if (!quizz_name) {
            alert('Phải đặt tên cho bài trắc nghiệm')
        }else {
            alert('Chưa có câu hỏi! và Phải đặt tên cho bài trắc nghiệm')
        }
    }else {
         for (let i = 0; i< list_question.length;i++){
            object_quizz.array_question.push(JSON.parse(list_question[i].value))
        }

        console.log(JSON.stringify(object_quizz))
        fetch('/api/add-quizz', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(object_quizz),
        }).then(response => {
            if (response.status === 200){
                alert('Thêm bài tập thành công!')
                window.location.href = '/admin';
            }else {
                alert('Có lỗi, vui lòng kiểm tra lại!')
            }
        })
    }
}
async function detail_subject(){
    let subject_id = document.getElementById('subject_id').textContent;
    let body_table = document.getElementById('body_table');
    let data_quizz = await (await fetch(`api/get-list-quizz?subject_id=${subject_id}`, {
        method: 'GET',
        })).json()
    if(data_quizz.status === 200){
        let stt = 0;
        data_quizz.data.map(quizz => {
            stt++
            body_table.innerHTML+= `
              <tr>
                <td style="text-align: center">${stt}</td>
                <td>${quizz.name}</td>
                <td>
                    <a href="/list-student?quizz_id=${quizz.id}" type="button" class="btn btn-outline-danger btn-sm">Xem danh sách học sinh</a>
                </td>
              </tr>
            `
        })
    }else {
        alert('load data fail')
    }
}

window.onload = detail_subject