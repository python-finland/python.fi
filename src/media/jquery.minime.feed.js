jQuery.fn.miniFeed = function (feedurl, options, callbackFunc) {
	top.feedOpt = jQuery.extend ({
		/**
		*
		*		 minime RSS and Atom Feed Reader
		*					ver 1.0.1
		*
		**/
		// Default options
		phpRepeater: "getfeed.php",		// XML - PHP repeater file for cross-domain errors against (Leave blank if extensions)
		timeout: 5000,					// Timeout
		limit: 10,						// Feed item limit
		getFeedTitle: true,				// Feed title visibility
		getItemTitle: true,				// Item title visibility
		getItemDate: true,				// Item date and time visibility
		getItemSummary: true,			// Item summary visibility
		getItemDescription: false,		// Item description visibility (only Atom feed)
		getItemLink: true,				// Item link visibility
		getAtomId: false,				// Item id visibility (only Atom feed)
		nextLinkText: "next &raquo;",	// Item hyperlink text 
		wrongXmlText: "Feeds are not given",									// Wrong RSS and Atom xml message
		timeoutText: "No responses were received within the specified time",	// Timeout message
		errorText: "The file is not found or network failure",					// HTTP and other error message
		notModifiedText: "The source has not changed since the last request",	// Not modified message
		parserErrorText: "Analytical error"										// XML Parser error message
	}, options);
		
		$(this).empty();
		// feedurl is empty
		if(!feedurl||feedurl=='') {
			$(this).append(top.feedOpt.errorText);
			return false;
		}
		if(feedurl.substr(0,7)=='http://'&&(top.feedOpt.phpRepeater!=''||top.feedOpt.phpRepeater!=null)) {
			feedurl = top.feedOpt.phpRepeater+'?url='+feedurl.substr(7);
		}
		top.selected = this;
		top.setHtml = '';
		$.ajax({
			type: "GET",
			url: feedurl,
			dataType: "xml",
 			timeout: top.feedOpt.timeout,
			success: function(xml) {
				if($(xml).children('rss').length>0) {
					// RSS feeds
					if(top.feedOpt.getFeedTitle) {
						var rssFeedTitle = $(xml).children('rss').children('channel').children('title').text();	
						top.setHtml += '<h4>'+rssFeedTitle+'</h4>';
					}
					top.setHtml += '<ul class="minimeFeed">';
						top.rsscounter = 0;
						$(xml).children('rss').children('channel').find('item').each(function() {
							// items to html
							top.rsscounter++;
							top.setHtml += '<li>';
							if($(this).children('title').length>0&&top.feedOpt.getItemTitle) {
								var itemTitle = $(this).children('title').text();
								top.setHtml += '<b>'+itemTitle+'</b>';
							}
							top.setHtml += '<div class="minimeFeedContent">';
							if($(this).children('pubDate').length>0&&top.feedOpt.getItemDate) {
								var itemDate = $(this).children('pubDate').text();
					  			top.setHtml += '<div class="minimeFeedDate">'+itemDate+'</div>';
							}
							if($(this).children('description').length>0&&top.feedOpt.getItemSummary) {
								var itemDescription = $(this).children('description').text();
								top.setHtml += '<div class="minimeFeedText">'+itemDescription+'</div>';
							}
							if($(this).children('link').length>0&&top.feedOpt.getItemLink) {
								var itemLinks = $(this).children('link').text();
								top.setHtml += '<a href="'+itemLinks+'" target="_blank">'+top.feedOpt.nextLinkText+'</a>';
							}
							top.setHtml += '</div>';
					  		top.setHtml += '</li>';
					  		// stopped
					  		if(top.rsscounter==top.feedOpt.limit) {
					  			return false;
					  		}
						});
						top.setHtml += '</ul>';
				}
								
				if($(xml).children('feed').length>0) {
					// ATOM feeds
					if(top.feedOpt.getFeedTitle) {
						var atomFeedTitle = $(xml).children('feed').children('title').text();
						top.setHtml += '<h4>'+atomFeedTitle+'</h4>';
					}
					top.setHtml += '<ul class="minimeFeed">';
						top.atomcounter = 0;
						$($(xml).children('feed').children('entry').get().reverse()).each(function() {
							// items to html
							top.atomcounter++;
							top.setHtml += '<li>';
							if($(this).children('title').length>0&&top.feedOpt.getItemTitle) {
								var itemTitle = $(this).children('title').text();
								top.setHtml += '<b>'+itemTitle+'</b>';
							}
							top.setHtml += '<div class="minimeFeedContent">';
							if($(this).children('updated').length>0&&top.feedOpt.getItemDate) {
								var itemDate = $(this).children('updated').text();
								top.setHtml += '<div class="minimeFeedDate">'+itemDate+'</div>';
							}
							if($(this).children('content').length>0&&top.feedOpt.getItemSummary) {
								// prkl mitä paskaa taas javascriptan kans.
								// tästäkö ne meinaa jotain serverikieltä, hä?
								// ei saa raw outputtia (innerHTML) XML inputista
								var itemSummary = $(this).children('content');
								var div = document.createElement("div");
								div.appendChild(itemSummary.get(0).childNodes[0].cloneNode(true));
								itemSummary = div.innerHTML;
								top.setHtml += '<div class="minimeFeedText">'+itemSummary+'</div>';
							}
							if($(this).children('description').length>0&&top.feedOpt.getItemDescription) {
								var itemDescription = $(this).children('description').text();
								top.setHtml += '<div class="minimeFeedText">'+itemDescription+'</div>';
							}
							if($(this).children('id').length>0&&top.feedOpt.getAtomId) {
								var atomItemId = $(this).children('id').text();
								top.setHtml += '<div class="minimeFeedAtomId">'+atomItemId+'</div>';
							}
							
							/*if($(this).children('link').length>0&&top.feedOpt.getItemLink) {
								var itemLink = $(this).children('link:first').attr('href');
								top.setHtml += '<a href="'+itemLink+'" target="_blank">'+top.feedOpt.nextLinkText+'</a>';
							}*/
							
							top.setHtml += '</div>';
					  		top.setHtml += '</li>';
					  		// stopped
					  		if(top.atomcounter==top.feedOpt.limit) {
					  			return false;
					  		}
						});
						top.setHtml += '</ul>';
				}
				// wrong xml
				if($(xml).children('rss').length==0&&$(xml).children('feed').length==0) {
					top.setHtml +=  top.feedOpt.wrongXmlText;	
				}
				$(top.selected).append(top.setHtml);
				if(typeof callbackFunc == 'function'){
					callbackFunc.call(this, xml);
				}
			},
			// Error Handling
			error: function (xhr, status, error) {
				if(xhr.statusText=='timeout') {
					top.setHtml +=  top.feedOpt.timeoutText;
				}
				if(xhr.statusText=='error') {
					top.setHtml +=  top.feedOpt.errorText;
				}
				if(xhr.statusText=='notmodified') {
					top.setHtml +=  top.feedOpt.notModifiedText;
				}
				if(xhr.statusText=='parsererror') {
					top.setHtml +=  top.feedOpt.parserErrorText;
				}
				$(top.selected).append(top.setHtml);
		    }
		});
	}

$(document).ready(function() {
	// Need to pipe through proxy due XSS not allowed in sites.google.com
	var url = "http://sites.google.com/a/python.fi/tiedotus/tiedotteet/posts.xml";
	var url = "/proxy?url=" + encodeURI(url);
	$('.posts').miniFeed(url, { limit: 10, getFeedTitle : false, getItemDate: false, getItemDescription : true});
});