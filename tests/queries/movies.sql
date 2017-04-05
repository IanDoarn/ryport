with s1 as(
select
	ac.first_name || ' ' || ac.last_name as full_name,
	fi.title,
	fi.description,
	fi.rating,
	fi.special_features,
	fi.film_id as f_id
from
	public.film_actor fa
		left join public.actor ac on fa.actor_id = ac.actor_id
		left join public.film fi on fa.film_id = fi.film_id
)
select
	s1.full_name,
	s1.title,
	s1.description,
	s1.rating,
	s1.special_features,
	ca.name
from
	s1
		left join public.film_category fca on fca.film_id = s1.f_id
		left join public.category ca on fca.category_id = ca.category_id
order by
	s1.title