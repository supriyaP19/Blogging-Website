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
insert into user values(13,'hrithik','hrithik@gmail.com','123','https://fvtvtf.blogspot.com/','hrkz blog',1);


comments
--------
insert into comments (comment_id,comment_postid,comment_userid,comment_content) values(1001,100,1,'Where can I get some?There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which dont look even slightly believable.');
insert into comments (comment_id,comment_postid,comment_userid,comment_content) values(1000,100,1,'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industryz standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially');

posts
-------
insert into posts (post_id,post_userid,post_published_on,post_content,post_title,post_status) values (100,1,datetime('now'),' Lorem <span style="color:green;">ipsum</span> dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.','Title 1','publish');
insert into posts (post_id,post_userid,post_published_on,post_content,post_title,post_status) values (101,1,datetime('now'),'Id eos sanctus quaerendum. Vix dicam verear cu, solum iudico detraxit an eum. In sea reque oratio dissentiet, tation nonumy expetenda sea eu. Diam movet voluptatibus ea est, ei mel liber aeque option','Title 2','publish');
insert into posts (post_id,post_userid,post_published_on,post_content,post_title,post_status) values (150,9,datetime('now'),'Id eos sanctus quaerendum. Vix dicam verear cu, solum iudico detraxit an eum. In sea reque oratio dissentiet, tation nonumy expetenda sea eu. Diam movet voluptatibus ea est, ei mel liber aeque option','think the way we do medicine now is very primitive, compared to what it could be','publish');
insert into posts (post_id,post_userid,post_published_on,post_content,post_title,post_status) values (151,9,datetime('now'),'<span style="color:pink;">The midterms were a feminist triumph: Tuesday was dominated by wins for women — women of color in particular — leading to a record-breaking number of women who will be serving in Congress. There was also a slew of notable firsts, including Alexandria Ocasio-Cortez (the youngest woman ever elected to Congress), Sharice Davids and Deb Haaland (the first Native American women), and Rashida Tlaib and Ilhan </span> Omar (the first Muslim women). As Cecile Richards put it, women were the heroes of this election.','Stop Trying to Flip Female Trump Supporters','publish');
insert into posts (post_id,post_userid,post_published_on,post_content,post_title,post_status) values (152,9,datetime('now'),'Michael Snyder, <strong> a Stanford biologist</strong> and pioneer in genomics, does. For the past several years, Snyder has been wearing a device he invented that measures the environment around him. Its part of his quest to learn how the environment impacts our health by studying what he calls','The Next Big Thing in Health is Your Exposome','draft');

followers
---------
insert into followers values(3,4);
insert into followers values(2,1);

follows
-------
insert into follows values(4,3);
insert into follows values(1,2);

