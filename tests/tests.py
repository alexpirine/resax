# coding: utf-8

import datetime

from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.test import TestCase
from django.test import utils
from django.utils import timezone
from resax import models
from resax.models import Model as M

def load_tests(loader, tests, ignore):
    import doctest

    tests.addTests(doctest.DocTestSuite(models))

    return tests

class TestActivityAndReservationType(TestCase):
    def setUp(self):
        self.cdh = M.Organisation.objects.create(name=u"Club de l'Hers")
        self.user1 = self.cdh.add_user()
        self.terrain = self.cdh.add_resource_type(u"Terrain")
        self.terrain_tennis = self.terrain.add_resource(u"Tennis", 3)
        self.terrain_basket = self.terrain.add_resource(u"Basketball")
        self.terrain_hand = self.terrain.add_resource(u"Handball")
        self.materiel = self.cdh.add_resource_type(u"Matériel")
        self.raquette = self.materiel.add_resource(u"Raquette", 10)

        self.cb = M.Organisation.objects.create(name=u"City Beast")
        self.salle = self.cb.add_resource_type(u"Salle")
        self.piscine = self.salle.add_resource(u"Piscine", 10)

    def test_setup_count(self):
        self.assertEqual(M.User.objects.count(), 1)
        self.assertEqual(M.Organisation.objects.count(), 2)
        self.assertEqual(M.ResourceType.objects.count(), 3)
        self.assertEqual(M.Resource.objects.count(), 5)

    def test_setup_relations(self):
        cdh = M.Organisation.objects.get(name=u"Club de l'Hers")
        cb = M.Organisation.objects.get(name=u"City Beast")

        self.assertEqual(cdh.users.count(), 1)
        self.assertEqual(cb.users.count(), 0)

        self.assertEqual([(rt.name, rt.resources.count()) for rt in cdh.resource_types.order_by('name')], [(u"Matériel", 1), (u"Terrain", 3)])
        self.assertEqual([(rt.name, rt.resources.count()) for rt in cb.resource_types.order_by('name')], [(u"Salle", 1)])

    def test_add_reservation_type_no_resources(self):
        reservation_type = self.cdh.add_reservation_type(u"Partie de Tennis")
        self.assertEqual(M.ReservationType.objects.count(), 1)
        self.assertEqual(reservation_type.resources.count(), 0)

    def test_add_reservation_type_one_resource(self):
        reservation_type = self.cdh.add_reservation_type(u"Partie de Tennis", self.terrain_tennis)
        self.assertEqual(M.ReservationType.objects.count(), 1)
        self.assertEqual(reservation_type.resources.count(), 1)

    def test_add_reservation_type_many_resources(self):
        reservation_type = self.cdh.add_reservation_type(u"Partie de Tennis", [self.terrain_tennis, self.raquette])
        self.assertEqual(M.ReservationType.objects.count(), 1)
        self.assertEqual(reservation_type.resources.count(), 2)

    def test_add_reservation_type_queryset_resources(self):
        reservation_type = self.cdh.add_reservation_type(u"Terrain de sport", M.Resource.objects.filter(resource_type__name = u"Terrain"))
        self.assertEqual(M.ReservationType.objects.count(), 1)
        self.assertEqual(reservation_type.resources.count(), 3)

    def test_add_reservation_type_wrong_resource(self):
        with self.assertRaises(ValidationError):
            self.cdh.add_reservation_type(u"Partie de Tennis", [self.piscine, self.raquette])
        self.assertEqual(M.ReservationType.objects.count(), 0)

    def test_add_activity_no_resources(self):
        activity = self.cdh.add_activity(u"Visite du club")
        self.assertEqual(M.Activity.objects.count(), 1)
        self.assertEqual(activity.resources.count(), 0)

    def test_add_activity_many_resources(self):
        activity = self.cdh.add_activity(u"Partie de Tennis", 1, {self.terrain_tennis: 1, self.raquette: 2})
        self.assertEqual(M.Activity.objects.count(), 1)
        self.assertEqual(activity.resources.count(), 2)
        self.assertEqual(activity.activity_resources.all().aggregate(v=Sum('quantity'))['v'], 3)

    def test_add_activity_too_many_resources(self):
        with self.assertRaises(ValidationError):
            activity = self.cdh.add_activity(u"Partie de Tennis à 10", 1, {self.terrain_tennis: 1, self.raquette: 20})
        self.assertEqual(M.Activity.objects.count(), 0)

        activity = self.cdh.add_activity(u"Partie de Tennis", 1, {self.terrain_tennis: 1, self.raquette: 4})
        self.assertEqual(M.Activity.objects.count(), 1)
        self.assertEqual(activity.activity_resources.get(resource = self.raquette).quantity, 4)

        raquette_ar = activity.add_resource(self.raquette, 6)
        self.assertEqual(activity.activity_resources.get(resource = self.raquette).quantity, 10)

        raquette_ar.set_quantity(9)
        self.assertEqual(activity.activity_resources.get(resource = self.raquette).quantity, 9)

        with self.assertRaises(ValidationError):
            raquette_ar.set_quantity(11)
        self.assertEqual(activity.activity_resources.get(resource = self.raquette).quantity, 9)

        with self.assertRaises(ValidationError):
            activity.add_resource(self.raquette, 2)
        self.assertEqual(activity.activity_resources.get(resource = self.raquette).quantity, 9)

    def test_add_activity_wrong_resource(self):
        with self.assertRaises(ValidationError):
            self.cdh.add_activity(u"Partie de Tennis", 1, {self.piscine: 1, self.raquette: 2})
        self.assertEqual(M.Activity.objects.count(), 0)


class TestCreatedOrganisation(TestCase):
    def setUp(self):
        M.Organisation.objects.create(name="Batb")
        M.Organisation.objects.create(name="Club de l'Hers")
        M.Organisation.objects.create(name="CityBeast")

    def test_organisation_created(self):
        batb = M.Organisation.objects.filter(name="Batb").first()
        cdh = M.Organisation.objects.filter(name="Club de l'Hers").first()
        citybeast = M.Organisation.objects.filter(name="CityBeast").first()

        self.assertIsNotNone(batb)
        self.assertIsNotNone(cdh)
        self.assertIsNotNone(citybeast)

    def test_destroy_organisation(self):
        cdh = M.Organisation.objects.filter(name="Club de l'Hers").first()
        cdh.delete()

        cdh = M.Organisation.objects.filter(name="Club de l'Hers").first()
        self.assertIsNone(cdh)


class TestCreatedUser(TestCase):
    def setUp(self):
        batb = M.Organisation.objects.create(name="Batb")
        batb.users.create()
        batb.users.create()
        batb.users.create()

    def test_user_created(self):
        batb = M.Organisation.objects.get(name="Batb")
        self.assertEqual(len(batb.users.all()), 3)


class TestCreatedRessource(TestCase):
    def setUp(self):
        batb = M.Organisation.objects.create(name="Batb")

        batb.resource_types.create(name="equipment")

        vehicle = batb.resource_types.create(name=u"vehicle")
        vehicle.resources.create(name=u"car")
        vehicle.resources.create(name=u"scooter")

    def test_resource_created(self):
        batb = M.Organisation.objects.filter(name="Batb").first()

        self.assertEqual(len(batb.resource_types.all()), 2)

        vehicule = M.ResourceType.objects.filter(name=u"vehicle").first()

        self.assertIsNotNone(vehicule)
        self.assertEqual(len(vehicule.resources.all()), 2)


class TestFlexiReservation(TestCase):
    def setUp(self):
        cdh = M.Organisation.objects.create(name="Club de l'Hers")
        cdh.users.create()

        equipment = cdh.resource_types.create(name="equipment")
        ball = equipment.resources.create(name=u"ball", stock=3)
        racquet = equipment.resources.create(name=u"racquet", stock=6)
        squash_racquet = equipment.resources.create(name=u"squash racquet", stock=4)

        squash_session = M.ReservationType.objects.create(name="squash session", organisation=cdh)
        squash_session.resources.add(squash_racquet)

        tennis_session = M.ReservationType.objects.create(name="tennis session", organisation=cdh)
        tennis_session.resources.add(ball)
        tennis_session.resources.add(racquet)

    def test_reservation_type_created(self):
        tennis_session = M.ReservationType.objects.filter(name="tennis session").first()
        self.assertIsNotNone(tennis_session)
        self.assertEqual(len(tennis_session.resources.all()), 2)

    def test_book_resources(self):
        cdh = M.Organisation.objects.get(name="Club de l'Hers")

        tennis_session = M.ReservationType.objects.filter(name="tennis session").first()

        ball = M.Resource.objects.get(name="ball")
        racquet = M.Resource.objects.get(name="racquet")
        user = cdh.users.all()[0]

        date_start = timezone.now() + datetime.timedelta(hours=1)
        date_stop = date_start + datetime.timedelta(hours=2)

        resources = dict([(ball, 1), (racquet, 2)])
        f_reservation = user.book_resources(tennis_session, date_start, date_stop, resources)

        self.assertEqual(len(user.flexi_reservations.all()), 1)
        self.assertEqual(ball.get_available_stock(date_start, date_stop), 2)
        self.assertEqual(racquet.get_available_stock(date_start, date_stop), 4)

    def test_too_many_flexi_reservation(self):
        cdh = M.Organisation.objects.get(name="Club de l'Hers")

        tennis_session = M.ReservationType.objects.filter(name="tennis session").first()

        equipment = cdh.resource_types.get(name="equipment")

        court = equipment.resources.create(name=u"court", stock=1)

        tennis_session.resources.add(court)

        ball = M.Resource.objects.get(name="ball")
        racquet = M.Resource.objects.get(name="racquet")

        user = cdh.users.all()[0]
        date_start = timezone.now() + datetime.timedelta(hours=1)
        date_stop = date_start + datetime.timedelta(hours=2)

        resources = dict([(ball, 1), (racquet, 2), (court, 1)])

        user.book_resources(tennis_session, date_start, date_stop, resources)
        with self.assertRaises(ValidationError):
            user.book_resources(tennis_session, date_start, date_stop, resources)

    def test_wrong_resource(self):
        cdh = M.Organisation.objects.get(name="Club de l'Hers")
        tennis_session = M.ReservationType.objects.filter(name="tennis session").first()

        ball = M.Resource.objects.get(name="ball")
        squash_racquet = M.Resource.objects.get(name="squash racquet")

        user = cdh.users.all()[0]

        date_start = timezone.now() + datetime.timedelta(hours=1)
        date_stop = date_start + datetime.timedelta(hours=2)

        resources = dict([(ball, 1), (squash_racquet, 2)])
        with self.assertRaises(ValidationError):
            user.book_resources(tennis_session, date_start, date_stop, resources)

    def test_remove_flexi_reservation(self):
        pass


class TestCreatedActivity(TestCase):
    def setUp(self):
        cdh = M.Organisation.objects.create(name="Club de l'Hers")

        cdh.activities.create(name="tennis", stock=3)

        equipment = cdh.resource_types.create(name="equipment")
        equipment.resources.create(name=u"ball", stock=3)
        equipment.resources.create(name=u"racquet", stock=6)

    def test_activity_created(self):
        cdh = M.Organisation.objects.get(name="Club de l'Hers")
        tennis = M.Activity.objects.filter(name=u"tennis").first()

        self.assertIsNotNone(tennis)
        self.assertEqual(len(cdh.activities.all()), 1)

        with self.assertRaises(M.Activity.DoesNotExist):
            M.Activity.objects.get(name=u"Badminton")

    def test_add_activity_resource(self):
        cdh = M.Organisation.objects.get(name="Club de l'Hers")

        tennis = M.Activity.objects.get(name=u"tennis", organisation=cdh)

        ball = M.Resource.objects.get(name="ball")
        racquet = M.Resource.objects.get(name="racquet")
        tennis.add_resource(ball, 2)
        tennis.add_resource(racquet, 1)

        self.assertEqual(ball.stock, 3)
        self.assertEqual(racquet.stock, 6)

        with self.assertRaises(ValidationError):
            tennis.add_resource(ball, 4)

    def test_remove_activity(self):
        pass


class TestReservation(TestCase):
    def setUp(self):
        cdh = M.Organisation.objects.create(name="Club de l'Hers")

        cdh.users.create()
        cdh.users.create()
        cdh.users.create()

        equipment = cdh.resource_types.create(name="equipment")
        ball = equipment.resources.create(name=u"ball", stock=3)
        racquet = equipment.resources.create(name=u"racquet", stock=6)

        tennis = cdh.activities.create(name="tennis", stock=1)
        tennis.add_resource(ball, 2)
        tennis.add_resource(racquet, 1)

    def test_remove_reservation(self):
        pass
