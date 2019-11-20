# -*- coding:utf-8 -*-
from enum import IntEnum


class CacheName(object):
    @staticmethod
    def get_user_total_pageviews_yesterday(user_id):
        return 'user_{0}_total_pageviews_yesterday'.format(user_id)

    @staticmethod
    def get_user_total_pageviews_this_month(user_id):
        return 'user_{0}_total_pageviews_this_month'.format(user_id)

    @staticmethod
    def get_article(article_id):
        return 'article_{0}'.format(article_id)

    @staticmethod
    def get_article_event(article_id):
        return 'article_event_{0}'.format(article_id)

    @staticmethod
    def get_article_favorite_user_list(article_id):
        return 'article_{0}_favorite'.format(article_id)

    @staticmethod
    def get_article_content(content_id):
        return 'article_content_{0}'.format(content_id)

    @staticmethod
    def get_article_content_list(article_id):
        return 'article_{0}_content_list'.format(article_id)

    @staticmethod
    def get_article_content_ok_list():
        return 'article_content_ok_list'

    @staticmethod
    def get_article_content_ng_list():
        return 'article_content_ng_list'

    @staticmethod
    def get_article_related_list(article_id, limit):
        return 'article_{0}_related_article_list_limit_{1}'.format(article_id, limit)

    @staticmethod
    def get_article_tag_list(article_id):
        return 'article_{0}_tag_list'.format(article_id)

    @staticmethod
    def get_article_access_history(article_id, page=1):
        return 'article_{0}_{1}_access_history'.format(article_id, page)

    @staticmethod
    def get_related_article_list(article_id):
        return 'related_article_{0}_list'.format(article_id)

    @staticmethod
    def get_cloudsearch_related_article_list(article_id):
        return 'cloudsearch_related_article_{0}_list'.format(article_id)

    @staticmethod
    def get_pickup_article_list(limit):
        return 'pickup_article_list_limit_{0}'.format(limit)

    @staticmethod
    def get_pickup_article_advertisement():
        return 'get_pickup_article_advertisement'

    @staticmethod
    def get_daily_popular_article_list(limit):
        return 'daily_popular_article_list_limit_{0}'.format(limit)

    @staticmethod
    def get_daily_popular_locations_article_list(location_id, limit):
        return 'daily_popular_article_list_location_{0}_limit_{1}'.format(location_id, limit)

    @staticmethod
    def get_daily_popular_tags_article_list(tag_id, limit):
        return 'daily_popular_article_list_tag_{0}_limit_{1}'.format(tag_id, limit)

    @staticmethod
    def get_featured_location_category_list():
        return 'featured_location_category_list'

    @staticmethod
    def get_location(location_id):
        return 'location_{0}'.format(location_id)

    @staticmethod
    def get_location_article_list(location_id):
        return 'location_{0}_articles'.format(location_id)

    @staticmethod
    def get_location_list():
        return 'location_list'

    @staticmethod
    def get_location_list_of_japan():
        return 'location_list_of_japan'

    @staticmethod
    def get_location_child_list():
        return 'location_child_list'

    @staticmethod
    def get_location_parent_list(location_id):
        return 'location_{0}_parent_list'.format(location_id)

    @staticmethod
    def get_location_child_id_list(location_id):
        return 'location_{0}_child_id_list'.format(location_id)

    @staticmethod
    def get_locations_structure():
        return 'locations_structure'

    @staticmethod
    def get_tag_parent_list(tag_id):
        return 'tag_{0}_parent_list'.format(tag_id)

    @staticmethod
    def get_tag_child_id_list(tag_id):
        return 'tag_{0}_child_id_list'.format(tag_id)

    @staticmethod
    def get_ng_tag_list():
        return 'ng_tag_list'.format()

    @staticmethod
    def get_feature(feature_id):
        return 'feature_{0}'.format(feature_id)

    @staticmethod
    def get_pickup_feature_list():
        return 'pickup_feature_list'

    @staticmethod
    def get_feature_parent_list(feature_id):
        return 'feature_{0}_parent_list'.format(feature_id)

    @staticmethod
    def get_scheduled_task_log(codename):
        return 'scheduled_task_{0}'.format(codename)

    @staticmethod
    def get_spot(spot_id):
        return 'spot_{0}'.format(spot_id)

    @staticmethod
    def get_enhanced_spot(spot_id):
        return 'spot_enhanced_{0}'.format(spot_id)

    @staticmethod
    def get_spot_images_list_main_types(spot_id):
        return 'spot_{0}_images_list_main_types'.format(spot_id)

    @staticmethod
    def get_spot_images_count(spot_id):
        return 'spot_{0}_images_count'.format(spot_id)

    @staticmethod
    def get_spot_images_count_main_types(spot_id):
        return 'spot_{0}_images_count_main_types'.format(spot_id)

    @staticmethod
    def get_spot_category_parent_list(spot_category_id):
        return 'spot_category_{0}_parent_list'.format(spot_category_id)

    @staticmethod
    def get_spot_categories_structure():
        return 'spot_categories_structure'

    @staticmethod
    def get_spot_existing(spot_id):
        return 'spot_{0}_existing'.format(spot_id)

    @staticmethod
    def get_spot_coupon(coupon_id):
        return 'spot_coupon_{0}'.format(coupon_id)

    @staticmethod
    def get_spot_content_list(spot_id):
        return 'spot_{0}_content_list'.format(spot_id)

    @staticmethod
    def get_spot_jalan_availability(spot_id, checkin, checkout):
        return 'spot_jalan_availability_{0}_{1}_{2}'.format(spot_id, checkin, checkout)

    @staticmethod
    def get_spot_rakuten_travel_availability(spot_id, checkin, checkout):
        return 'spot_rakuten_travel_availability_{0}_{1}_{2}'.format(spot_id, checkin, checkout)

    @staticmethod
    def get_spot_booking_availability(spot_id, checkin, checkout):
        return 'spot_booking_availability_{0}_{1}_{2}'.format(spot_id, checkin, checkout)

    @staticmethod
    def get_spot_ikyu_availability(spot_id, checkin, checkout):
        return 'spot_ikyu_availability_{0}_{1}_{2}'.format(spot_id, checkin, checkout)

    @staticmethod
    def get_spot_expedia_availability(spot_id, checkin, checkout):
        return 'spot_expedia_availability_{0}_{1}_{2}'.format(spot_id, checkin, checkout)

    @staticmethod
    def get_spot_hotels_com_availability(spot_id, checkin, checkout):
        return 'spot_hotels_com_availability_{0}_{1}_{2}'.format(spot_id, checkin, checkout)

    @staticmethod
    def get_spot_jtb_availability(spot_id, checkin, checkout):
        return 'spot_jtb_availability_{0}_{1}_{2}'.format(spot_id, checkin, checkout)

    @staticmethod
    def get_spot_access_history(spot_id, page=1):
        return 'spot_{0}_{1}_access_history'.format(spot_id, page)

    @staticmethod
    def get_infosource():
        return 'infosource'

    @staticmethod
    def get_jack_ad():
        return 'jack_ad'

    @staticmethod
    def get_jack_ad_id(jack_ad_id):
        return 'jack_ad_{}'.format(jack_ad_id)

    @staticmethod
    def get_in_app_notification_article_top():
        return 'in_app_notification_article_top'

    @staticmethod
    def get_in_app_notification_article_under_description():
        return 'in_app_notification_article_under_description'

    @staticmethod
    def get_in_app_notification_article_bottom():
        return 'in_app_notification_article_bottom'

    @staticmethod
    def get_in_app_notification_article_fixed():
        return 'in_app_notification_article_fixed'

    @staticmethod
    def get_admin_count(query):
        return 'admin_count_{}'.format(query)

    @staticmethod
    def get_proxy_list():
        return 'proxy_list'

    @staticmethod
    def get_cookies(token):
        return 'cookies_{}'.format(token)

    @staticmethod
    def get_site_id(site_id):
        return 'site_id_{}'.format(site_id)

    @staticmethod
    def get_site_domain(domain):
        return 'site_domain_{}'.format(domain)

    @staticmethod
    def get_article_site(article_id):
        return 'article_site_{}'.format(article_id)

    @staticmethod
    def get_area_category_spots(location_id, category_id, scene_id, page, order):
        if category_id:
            if scene_id:
                return 'area_category_scene_spots_{0}_{1}_{2}_{3}_{4}'.format(location_id, category_id, scene_id, page, order)
            return 'area_category_spots_{0}_{1}_{2}_{3}'.format(location_id, category_id, page, order)
        else:
            if scene_id:
                return 'area_category_scene_spots_{0}_{1}_{2}_{3}'.format(location_id, scene_id, page, order)
            return 'area_category_spots_{0}_{1}_{2}'.format(location_id, page, order)

    @staticmethod
    def get_area_category_articles(location_id, category_id, scene_id, page):
        if category_id:
            if scene_id:
                return 'area_category_scene_articles_{0}_{1}_{2}_{3}'.format(location_id, category_id, scene_id, page)
            return 'area_category_articles_{0}_{1}_{2}'.format(location_id, category_id, page)
        else:
            if scene_id:
                return 'area_category_scene_articles_{0}_{1}_{2}'.format(location_id, scene_id, page)
            return 'area_category_articles_{0}_{1}'.format(location_id, page)

    @staticmethod
    def get_area_category_recommended_articles(location_id, category_id):
        if category_id:
            return 'area_category_recommended_articles_{0}_{1}'.format(location_id, category_id)
        else:
            return 'area_category_recommended_articles_{0}'.format(location_id)

    @staticmethod
    def get_search_service():
        return 'search_service'


class RedisDatabaseEnum(IntEnum):
    general_cache = 0  # this won't be referenced since the value is implanted directly in the settings files.
    counter = 1
    buffer = 2
