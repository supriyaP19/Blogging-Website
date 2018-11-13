theme
-------
insert into theme values(1);
insert into theme values(2);
insert into theme values(3);

user
-------
insert into user values(1,'supriya19','sup@gmail.com','123','sup.com','Sups blog',1);
insert into user values(2,'harshita12','hotness@gmail.com','123','papaya.com','Papayaz blog',1);
insert into user values(3,'rajat09','gadha@gmail.com','123','gadha_verma.com','rjz blog',3);
insert into user values(4,'shruti19','tooty_fruity@gmail.com','123','fruity.com','Shrutiz blog',2);
insert into user values(12,'amishapatel','amisha@gmail.com','123','https://fvtvtf.blogspot.com/','amishaz blog',1);

comments
--------
insert into comments (comment_id,comment_postid,comment_userid,comment_content) values(1001,100,1,'Where can I get some?There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which dont look even slightly believable.');
insert into comments (comment_id,comment_postid,comment_userid,comment_content) values(1000,100,1,'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industryz standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially');

posts
-------
insert into posts (post_id,post_userid,post_published_on,post_content,post_title) values (100,1,datetime('now'),' Lorem <span style="color:green;">ipsum</span> dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.','Title 1');
insert into posts (post_id,post_userid,post_published_on,post_content,post_title) values (101,1,datetime('now'),'Id eos sanctus quaerendum. Vix dicam verear cu, solum iudico detraxit an eum. In sea reque oratio dissentiet, tation nonumy expetenda sea eu. Diam movet voluptatibus ea est, ei mel liber aeque option','Title 2');

followers
---------
insert into followers values(3,4);
insert into followers values(2,1);

follows
-------
insert into follows values(4,3);
insert into follows values(1,2);

