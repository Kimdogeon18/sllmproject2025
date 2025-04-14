function generateText() {
    // 입력값 가져오기
    const inputText = document.getElementById('userInput').value;

    // 서버에 POST 요청
    $.ajax({
        url: 'http://localhost:8000/generate',  // 서버 URL
        type: 'POST',  // HTTP 메서드 (POST)
        contentType: 'application/json',  // 요청 본문의 콘텐츠 타입
        data: JSON.stringify({ text: inputText }),  // 본문 데이터 (입력 텍스트)
        success: function(response) {
            console.log('응답:', response);  // 응답을 콘솔에 출력
            document.getElementById('Output').value = response.generated_text;
        },
        error: function(xhr, status, error) {
            // 오류 발생 시 처리
            console.error('에러 발생:', error);
            document.getElementById('Output').value = '오류가 발생했습니다. 콘솔을 확인해주세요.';
        }
    });
}