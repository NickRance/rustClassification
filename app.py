from flickr_rust import *

flickr_rustSetId = 72157623812855325
flickr_nonrustGroupId = '54054161@N00'#"shinymetalthings"

if __name__=="__main__":
	#Downloads
	#flickr_walk(keyword="stainlesssteel",limit=1,color_codes='d')
	#Download from shiny metal things
	flickr_group(keyword="",limit=100,group_id=flickr_nonrustGroupId)
	#Downloads Rust Image Set
	flickr_set(limit=100,set_id=flickr_rustSetId)