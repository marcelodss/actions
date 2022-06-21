from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save

def cria_profile(sender, instance, created, **kwags):
    print('\nSignal chamado com sucesso.\n')
    print("sender ", sender)
    print("instance ", instance)
    print("created ", created)
    print("kwags", kwags)
    if created:
        print('\n>> Signal chamado com sucesso ao criar usuario\n')
        Profile.objects.create(usuario=instance, telefone="Criou 0000")
    else:
        print('\n>> Signal chamado com sucesso ao alterar usuario\n')
        if not hasattr(instance, "profile"):
            print('\>>>>> instance, "profile" Não existe\n')
            Profile.objects.create(usuario=instance, telefone="Alterou 1111")
        else:
            print('\>>>>> instance, "profile" Existe\n')
            Profile.objects.update(telefone="Alterou 2222")

post_save.connect(cria_profile, sender=User)